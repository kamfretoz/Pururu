import logging
import re
from typing import Optional


import hikari
import lightbulb
import spotipy
from lightbulb.utils import nav, pag
from spotipy.oauth2 import SpotifyClientCredentials
from utils.const import LAVALINK_SERVER, LAVALINK_PASSWORD, \
        LAVALINK_PORT, TIME_REGEX, SPOTCLIENT_ID, SPOTCLIENT_SECRET

import lavasnek_rs

music_plugin = lightbulb.Plugin("music", "Music Related commands", include_datastore=True)
music_plugin.add_checks(lightbulb.checks.guild_only)

class EventHandler:
    """Events from the Lavalink server"""

    async def track_start(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        song = await music_plugin.d.lavalink.decode_track(event.track)
        embed = hikari.Embed(title="**Now Playing.**", description=f"[{song.title}]({song.uri})", color=0x00FF00)
        embed.add_field(name="Artist", value=song.author, inline=False)
        identifier = song.identifier
        thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
        embed.set_thumbnail(thumb)
        logging.info("Track started on guild: %s", event.guild_id)

    async def track_finish(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        guild_node = await lavalink.get_guild_node(event.guild_id)
        if not guild_node or not guild_node.now_playing and len(guild_node.queue) == 0:
            if event.guild_id is not None:
                await music_plugin.bot.update_voice_state(event.guild_id, None)
                await music_plugin.d.lavalink.wait_for_connection_info_remove(event.guild_id)
            await music_plugin.d.lavalink.destroy(event.guild_id)
            await music_plugin.d.lavalink.remove_guild_from_loops(event.guild_id)
            await music_plugin.d.lavalink.remove_guild_node(event.guild_id)
            logging.info(f"Track finished on guild: {event.guild_id}")

    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
        logging.warning("Track exception event happened on guild: %d", event.guild_id)

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)

async def _join(ctx: lightbulb.Context) -> Optional[hikari.Snowflake]:
    assert ctx.guild_id is not None

    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return None

    channel_id = voice_state.channel_id

    assert channel_id is not None

    await music_plugin.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
    connection_info = await music_plugin.d.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

    await music_plugin.d.lavalink.create_session(connection_info)

    return channel_id


@music_plugin.listener(hikari.ShardReadyEvent)
async def start_lavalink(event: hikari.ShardReadyEvent) -> None:
    """Event that triggers when the hikari gateway is ready."""

    builder = (
        # TOKEN can be an empty string if you don't want to use lavasnek's discord gateway.
        lavasnek_rs.LavalinkBuilder(event.my_user.id, "")
        # This is the default value, so this is redundant, but it's here to show how to set a custom one.
            .set_host(LAVALINK_SERVER)
            .set_port(int(LAVALINK_PORT))
            .set_password(LAVALINK_PASSWORD)
            .set_is_ssl(False)
            .set_start_gateway(False)
    )

    builder.set_start_gateway(False)

    lava_client = await builder.build(EventHandler())

    music_plugin.d.lavalink = lava_client


@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("join", "Joins the voice channel you are in.", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def join(ctx: lightbulb.Context) -> None:
    """Joins the voice channel you are in."""
    channel_id = await _join(ctx)

    if channel_id:
        await ctx.respond(f"Joined <#{channel_id}>")

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("query", "The query to search for.", str,  modifier=lightbulb.OptionModifier.CONSUME_REST, autocomplete=True, required=True, pass_options = True)
@lightbulb.command("play", "Searches the query on youtube, or adds the URL to the queue.", aliases=["p", "pl"], pass_options=True, auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def play(ctx: lightbulb.Context, query: str) -> None:
    """Searches the query on youtube, or adds the URL to the queue."""

    if not query:
        await ctx.respond("Please specify a query.")
        return None

    con = music_plugin.d.lavalink.get_guild_gateway_connection_info(ctx.guild_id)
    # Join the user's voice channel if the bot is not in one.
    if not con:
        await _join(ctx)

    if "https://open.spotify.com/playlist/" in query:
        await ctx.respond(
            embed=hikari.Embed(title="Spotify Playlist are not currently supported.", color=ctx.author.accent_color))
        return

    if "https://open.spotify.com/track" in query:
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID, client_secret=SPOTCLIENT_SECRET))
        track_link = f"{query}"
        track_id = track_link.split("/")[-1].split("?")[0]
        track = f"spotify:track:{track_id}"
        spotifytrack = sp.track(track)
        trackname = spotifytrack['name'] + " " + spotifytrack["artists"][0]["name"]
        result = f"ytmsearch:{trackname}"
        query_information = await music_plugin.d.lavalink.get_tracks(result)
        await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
        emb = hikari.Embed(title="Added Song To The Queue", color=ctx.author.accent_color)
        emb.add_field(name="Name",
                        value=f"[{query_information.tracks[0].info.title}]({query_information.tracks[0].info.uri})",
                        inline=False)
        emb.add_field(name="Artist", value=f"{query_information.tracks[0].info.author}", inline=False)
        identifier = query_information.tracks[0].info.identifier
        thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
        emb.set_thumbnail(thumb)
        length = divmod(query_information.tracks[0].info.length, 60000)
        emb.add_field(name="Duration", value=f"{int(length[0])}:{round(length[1] / 1000):02}")
        await ctx.respond(embed=emb)
        return

    # Search the query, auto_search will get the track from a url if possible, otherwise,
    # it will search the query on youtube.
    query_information = await music_plugin.d.lavalink.auto_search_tracks(query)


    if query_information:
        try:
            name = query_information.tracks[0].info.title
            identifier = query_information.tracks[0].info.identifier
            uri = query_information.tracks[0].info.uri
            thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
            length = divmod(query_information.tracks[0].info.length, 60000)
        except IndexError:
            await ctx.respond("Could not find any video of the search query.")
            return
    else: # tracks is empty
        await ctx.respond("Could not find any video of the search query.")
        return

    try:
        # `.requester()` To set who requested the track, so you can show it on now-playing or queue.
        # `.queue()` To add the track to the queue rather than starting to play the track now.
        await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
    except lavasnek_rs.NoSessionPresent:
        await ctx.respond(f"BOT is not currently in any voice channel!")
        return

    emb = hikari.Embed(title="**Added to queue!**", color=ctx.author.accent_color)
    emb.add_field(name="Name", value=f"[{name}]({uri})", inline=False)
    emb.add_field(name="Author", value=query_information.tracks[0].info.author, inline=False)
    emb.add_field(name="Length", value=f"{int(length[0])}:{round(length[1] / 1000):02}", inline=False)
    emb.set_thumbnail(thumb)

    await ctx.respond(embed=emb)
    
@play.autocomplete("query")
async def play_autocomplete(opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction):
    query = await music_plugin.d.lavalink.auto_search_tracks(opt.value)
    return [track.info.title for track in query.tracks[:5]]

@music_plugin.command()
@lightbulb.command("replay", "Replays the current song.", auto_defer=True, aliases=["rp"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def replay(ctx: lightbulb.Context) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return

    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    await music_plugin.d.lavalink.seek_millis(ctx.guild_id, 0000)
    embed = hikari.Embed(title=f"**Replaying {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("index", "Index for the song you want to remove.", int, required = True, pass_options = True)
@lightbulb.command("remove", "Removes a song from the queue.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def remove(ctx: lightbulb.Context, index: int) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return

    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if index == 0:
        embed = hikari.Embed(title=f"**You cannot remove a song that is currently playing.**",color=0xC80000)
        return await ctx.respond(embed=embed)
    try:
        queue = node.queue
        song_to_be_removed = queue[index]
    except:
        embed = hikari.Embed(title=f"**Incorrect position entered.**",color=0xC80000)
        return await ctx.respond(embed=embed)
    try:
        queue.pop(index)
    except:
        pass
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    embed = hikari.Embed(title=f"**Removed {song_to_be_removed.track.info.title}.**",color=0x6100FF,)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.command("leave", "leaves your voice channel.", auto_defer=True, aliases=["stop"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def leave(ctx: lightbulb.Context) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return

    await music_plugin.d.lavalink.destroy(ctx.guild_id)
    if ctx.guild_id is not None:
        await music_plugin.bot.update_voice_state(ctx.guild_id, None)
        await music_plugin.d.lavalink.wait_for_connection_info_remove(ctx.guild_id)

    await music_plugin.d.lavalink.remove_guild_from_loops(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_node(ctx.guild_id)
    embed = hikari.Embed(title="**Stopped the music left voice channel.**", colour=ctx.author.accent_color)
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.option("percentage", "What to change the volume to.", int, max_value=200, min_value=0, default=100)
@lightbulb.command("volume", "Change the volume.", auto_defer=True, aliases=["v"], pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def volume(ctx: lightbulb.Context, percentage: int) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    embed = hikari.Embed(title=f"**Volume is now at {percentage}%**", color=ctx.author.accent_color)

    if isinstance(ctx, lightbulb.PrefixContext):
        if percentage > 1000:
            percentage = 1000

    if percentage > 200:
        embed.add_field("**WARNING!**",
                        "**You have gone above and beyond the safe threshold of the volume (200%).** \n*May God have mercy on your ears.*")

    await music_plugin.d.lavalink.volume(ctx.guild_id, percentage)
    node.set_data({"volume": percentage})

    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.option("time", "What time you would like to seek to.", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("seek", "Seek to a specific point in a song.", auto_defer=True, aliases=["se"], pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def seek(ctx: lightbulb.Context, time) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    if not (match := re.match(TIME_REGEX, time)):
        embed = hikari.Embed(title="**Invalid time entered.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    if match.group(3):
        secs = (int(match.group(1)) * 60) + (int(match.group(3)))
    else:
        secs = int(match.group(1))
    await music_plugin.d.lavalink.seek_millis(ctx.guild_id, secs * 1000)

    embed = hikari.Embed(title=f"**Seeked {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)

        embed.add_field(name="Current Position", value=f"{time}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("skip", "Skips the current song.", aliases=["sk"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def skip(ctx: lightbulb.Context) -> None:
    """Skips the current song."""
    
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return None

    skip = await music_plugin.d.lavalink.skip(ctx.guild_id)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    embed = hikari.Embed(colour=ctx.author.accent_color)

    if not skip:
        embed.add_field(name="Skipped", value="Nothing to skip")
    else:
        # If the queue is empty, the next track won't start playing (because there isn't any),
        # so we stop the player.
        if not node.queue and not node.now_playing:
            await music_plugin.d.lavalink.stop(ctx.guild_id)
        embed.add_field(name="Skipped", value=f"{skip.track.info.title}")
        
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("pause", "Pauses the currently playing track.", auto_defer=True, aliases=["ps"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pause(ctx: lightbulb.Context) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    await music_plugin.d.lavalink.pause(ctx.guild_id)
    embed = hikari.Embed(title=f"**Paused {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played",
                        value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("resume", "Resumes playing the currently playing track.", auto_defer=True, aliases=["unpause", "rs"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def resume(ctx: lightbulb.Context) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    await music_plugin.d.lavalink.resume(ctx.guild_id)
    embed = hikari.Embed(title=f"**Resumed {node.now_playing.track.info.title}.**", colour=ctx.author.accent_color)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played",
                        value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)


@music_plugin.command()
@lightbulb.command("nowplaying", "See what's currently playing.", auto_defer=True, aliases=["np", "playing"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def now_playing(ctx: lightbulb.Context) -> None:
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return

    if node.is_paused:
        status = "**⏸ Paused**"
    else:
        status = "**▶ Currently Playing**"

    embed = hikari.Embed(title=status, color=ctx.author.accent_color)
    embed.add_field(name="Name", value=f"[{node.now_playing.track.info.title}]({node.now_playing.track.info.uri})",
                    inline=False)
    embed.add_field(name="Artist", value=node.now_playing.track.info.author, inline=False)
    identifier = node.now_playing.track.info.identifier
    thumb = f"http://img.youtube.com/vi/{identifier}/0.jpg"
    embed.set_thumbnail(thumb)
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played",
                        value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}")
    except:
        pass
    
    
    volume = node.get_data().get("volume")
    
    if not volume:
        volume = 100
    embed.add_field(name="Volume", value=f"{volume}%")
    await ctx.respond(embed=embed)
    
@music_plugin.command()
@lightbulb.command("queue", "Shows you the queue.", aliases=["q", "que"], auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def queue(ctx: lightbulb.Context) -> None:
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    if len(node.queue) == 1:
        embed = hikari.Embed(title="**The queue is currently empty.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None

    songs = [
        f'[{tq.track.info.title} - {tq.track.info.author}]({tq.track.info.uri}) ({int(divmod(tq.track.info.length, 60000)[0])}:{round(divmod(tq.track.info.length, 60000)[1] / 1000):02})'
        for i, tq in enumerate(node.queue[1:], start=1)]

    lst = pag.EmbedPaginator()

    @lst.embed_factory()
    def build_embed(page_index, page_content):
        emb = hikari.Embed(title=f"Current Queue (Page {page_index})", description=page_content,
                            color=ctx.author.accent_color)
        return emb

    i = 1
    for track in songs:
        lst.add_line(f"**{i}.** {track}")
        i += 1

    navigator = nav.ButtonNavigator(lst.build_pages())
    await navigator.run(ctx)

@music_plugin.command()
@lightbulb.option("new_position", "The songs new position in the queue.", int, required=True)
@lightbulb.option("current_position", "The songs current position in the queue.", int, required=True)
@lightbulb.command("move", "Move a song to a different position in the queue.", auto_defer=True, aliases=["mv"],
                    pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def move(ctx: lightbulb.Context, current_position, new_position) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    new_index = new_position
    old_index = current_position
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not len(node.queue) >= 1:
        embed = hikari.Embed(title=f"**There is only 1 song in the queue.**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    queue = node.queue
    song_to_be_moved = queue[old_index]
    try:
        queue.pop(old_index)
        queue.insert(new_index, song_to_be_moved)
    except:
        embed = hikari.Embed(title=f"**Incorrect position entered.**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    embed = hikari.Embed(title=f"**Moved {song_to_be_moved.track.info.title} to position #{new_index}.**",
                        color=ctx.author.accent_color)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.option("position", "The song's position in the queue.", int, required=True)
@lightbulb.command("skipto", "skip to a different song in the queue.", auto_defer=True, aliases=["skto"],
                    pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def skipto(ctx: lightbulb.Context, position: int) -> None:
    if not (voice_state := ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)):
        await ctx.respond("Connect to a voice channel first.")
        return
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    index = position
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if index == 0:
        embed = hikari.Embed(title=f"**You cannot move to a song that is currently playing.**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    if index == 1:
        embed = hikari.Embed(title=f"**Skipping to the next song.**", color=0xC80000)
        await ctx.respond(embed=embed)
        await music_plugin.d.lavalink.skip(ctx.guild_id)
        return
    try:
        queue = node.queue
        song_to_be_skipped = queue[index]
    except:
        embed = hikari.Embed(title=f"**Incorrect position entered.**", color=0xC80000)
        await ctx.respond(embed=embed)
        return
    queue.insert(1, queue[index])
    queue.pop(index)
    queue.pop(index)
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    await music_plugin.d.lavalink.skip(ctx.guild_id)
    embed = hikari.Embed(title=f"**Skipped to {song_to_be_skipped.track.info.title}.**", color=ctx.author.accent_color)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.add_checks(lightbulb.owner_only)  # Optional
@lightbulb.option(
    "args", "The arguments to write to the node data.", required=False, modifier=lightbulb.OptionModifier.CONSUME_REST
)
@lightbulb.command("nodedata", "Load or read data from the node.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def data(ctx: lightbulb.Context) -> None:
    """Load or read data from the node.

    If just `data` is ran, it will show the current data, but if `data <key> <value>` is ran, it
    will insert that data to the node and display it."""

    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node:
        await ctx.respond("No node found.")
        return None

    if args := ctx.options.args:
        args = args.split(" ")

        if len(args) == 1:
            node.set_data({args[0]: args[0]})
        else:
            node.set_data({args[0]: args[1]})
    await ctx.respond(node.get_data())

@music_plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    music_plugin.d.lavalink.raw_handle_event_voice_state_update(
        event.state.guild_id,
        event.state.user_id,
        event.state.session_id,
        event.state.channel_id,
    )


@music_plugin.listener(hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: hikari.VoiceServerUpdateEvent) -> None:
    await music_plugin.d.lavalink.raw_handle_event_voice_server_update(event.guild_id, event.endpoint, event.token)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(music_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(music_plugin)
