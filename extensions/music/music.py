import logging
from typing import Optional
import hikari
import lightbulb
import lavasnek_rs
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import os
from datetime import date
import dotenv
from lightbulb.ext import filament
import miru
from miru.ext import nav

dotenv.load_dotenv()

HIKARI_VOICE = False
URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
SPOTCLIENT_ID=os.getenv("SPOTID")
SPOTCLIENT_SECRET=os.getenv("SPOTSECRET")
TOKEN=os.getenv("BOT_TOKEN")
LAVALINK_SERVER=os.getenv("LAVA_SRV")
LAVALINK_PORT=os.getenv("LAVA_PORT")
LAVALINK_PASSWORD=os.getenv("LAVA_PASS")

music_plugin = lightbulb.Plugin("music", "Music Related commands", include_datastore=True)
class EventHandler:

    async def track_start(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        logging.info(f"Track started on guild: {event.guild_id}")
        

    async def track_finish(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        guild_node = await lavalink.get_guild_node(event.guild_id)
        loop_enabled = guild_node.get_data().get("loop")
        if loop_enabled:
            song = await music_plugin.d.lavalink.decode_track(event.track)
            result = await music_plugin.d.lavalink.get_tracks(song.uri)
            await lavalink.play(event.guild_id, result.tracks[0]).queue()
            return
        
        if not guild_node or not guild_node.now_playing and len(guild_node.queue) == 0:
            await music_plugin.d.lavalink.destroy(event.guild_id)
            await music_plugin.d.lavalink.leave(event.guild_id)
            await music_plugin.d.lavalink.remove_guild_node(event.guild_id)
            await music_plugin.d.lavalink.remove_guild_from_loops(event.guild_id)
            return


    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
        logging.warning(f"Track exception event happened on guild: {event.guild_id}")
        

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)

async def _join(ctx: lightbulb.Context) -> Optional[hikari.Snowflake]:
    assert ctx.guild_id is not None

    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]

    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None

    channel_id = voice_state[0].channel_id

    if HIKARI_VOICE:
        assert ctx.guild_id is not None

        await music_plugin.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True, self_mute=True)
        connection_info = await music_plugin.d.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

    else:
        try:
            connection_info = await music_plugin.d.lavalink.join(ctx.guild_id, channel_id)
        except TimeoutError:
            await ctx.respond("It seems that there's an issue. I might not have the right permissions.")
            return None

    await music_plugin.d.lavalink.create_session(connection_info)

    return channel_id

@music_plugin.listener(hikari.ShardReadyEvent)
async def start_lavalink(event: hikari.ShardReadyEvent) -> None:
    builder = (
        lavasnek_rs.LavalinkBuilder(event.my_user.id, TOKEN)
        .set_host(LAVALINK_SERVER).set_port(int(LAVALINK_PORT)).set_password(LAVALINK_PASSWORD)
    )
    if HIKARI_VOICE:
        builder.set_start_gateway(False)
    lava_client = await builder.build(EventHandler())
    music_plugin.d.lavalink = lava_client

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("join", "Joins your voice channel", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def join(ctx: lightbulb.Context) -> None:
    channel_id = await _join(ctx)
    if channel_id:
        embed = hikari.Embed(title="**Joined voice channel.**", colour=0x6100FF)
        await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("leave", "leaves your voice channel.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def leave(ctx: lightbulb.Context) -> None:
    await music_plugin.d.lavalink.destroy(ctx.guild_id)
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if HIKARI_VOICE:
        if ctx.guild_id is not None:
            await music_plugin.bot.update_voice_state(ctx.guild_id, None)
            await music_plugin.d.lavalink.wait_for_connection_info_remove(ctx.guild_id)
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0x6100FF)
        await ctx.respond(embed=embed)
        return
    else:
        await music_plugin.d.lavalink.leave(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_node(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_from_loops(ctx.guild_id)
    embed = hikari.Embed(title="**Left voice channel.**", colour=0x6100FF)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("query", "The name of the song (or url) that you want to play", modifier=lightbulb.OptionModifier.CONSUME_REST, required = True)
@lightbulb.command("play", "searches for your song.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
@filament.utils.pass_options
async def play(ctx: lightbulb.Context, query) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    if not query:
        embed = hikari.Embed(title="**Please enter a song to play.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    await _join(ctx)
    if "https://open.spotify.com/playlist" in query:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
        playlist_link = f"{query}"
        playlist_URI = playlist_link.split("/")[-1].split("?")[0]
        track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
        for track in sp.playlist_tracks(playlist_URI)["items"]:
            track_name = track["track"]["name"]
            track_artist = track["track"]["artists"][0]["name"]
            queryfinal = f"{track_name} " + " " + f"{track_artist}" 
            result = f"ytmsearch:{queryfinal}"
            query_information = await music_plugin.d.lavalink.get_tracks(result)
        try:
            await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
        except:
            pass
        embed=hikari.Embed(title="**Added Playlist To The Queue.**", color=0x6100FF)
        return await ctx.respond(embed=embed)
    if "https://open.spotify.com/album" in query:	
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
        album_link = f"{query}"
        album_id= album_link.split("/")[-1].split("?")[0]
        for track in sp.album_tracks(album_id)["items"]:
            track_name = track["name"]
            track_artist = track["artists"][0]["name"]
            queryfinal = f"{track_name} " + f"{track_artist}" 
            result = f"ytmsearch:{queryfinal}"
            query_information = await music_plugin.d.lavalink.get_tracks(result)
        try:
            await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
        except:
            pass
        embed=hikari.Embed(title="**Added Album To The Queue.**", color=0x6100FF)
        return await ctx.respond(embed=embed)
    if "https://open.spotify.com/track" in query:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
        track_link = f"{query}"
        track_id= track_link.split("/")[-1].split("?")[0]
        track = f"spotify:track:{track_id}"
        spotifytrack = sp.track(track)
        trackname = spotifytrack['name'] + " " + spotifytrack["artists"][0]["name"]
        result = f"ytmsearch:{trackname}"
        query_information = await music_plugin.d.lavalink.get_tracks(result)   
        await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
        embed=hikari.Embed(title="Added Song To The Queue",color=0x6100FF) 
        return await ctx.respond(embed=embed) 
    if not re.match(URL_REGEX, query):
      sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
      results = sp.search(q=f'{query}', limit=1)
      for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]
      try:
        queryfinal = f"{querytrack}" + " " + f"{queryartist}"
      except:
        embed = hikari.Embed(title="**Unable to find any songs! Please try to include the song's artists name as well.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
      result = f"ytmsearch:{queryfinal}"
      query_information = await music_plugin.d.lavalink.get_tracks(result)
    else:
        query_information = await music_plugin.d.lavalink.get_tracks(query)
    if not query_information.tracks:
        embed = hikari.Embed(title="**Unable to find any songs! Please try to include the song's artists name as well.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
     sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
     results = sp.search(q=f'{query}', limit=1)
     for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]	
     embed1=hikari.Embed(title="**Now Playing**",color=0x6100FF)
     try:
        embed1.add_field(name="Name", value=f"{[querytrack]}({track['external_urls']['spotify']})", inline=False)
     except:
        embed1.add_field(name="Name", value=f"{query_information.tracks[0].info.title}", inline=False)
     try:
        embed1.add_field(name="Artist", value=f"{[queryartist]}({track['artists'][0]['external_urls']['spotify']})", inline=False)
     except:
        embed1.add_field(name="Artist", value=f"{query_information.tracks[0].info.author}", inline=False)
     try:
        embed1.add_field(name="Album", value=f"{[track['album']['name']]}({track['album']['external_urls']['spotify']})", inline=False)
     except:
        pass
     try:
        length = divmod(query_information.tracks[0].info.length, 60000)
        embed1.add_field(name="Duration", value=f"{int(length[0])}:{round(length[1]/1000):02}")
     except:
        pass
     try:
        embed1.add_field(name="Release Date", value=f"{track['album']['release_date']}", inline=False)
     except:
        pass
     try:
        embed1.set_thumbnail(f"{track['album']['images'][0]['url']}")
     except:
        pass
     await ctx.respond(embed=embed1)
    else:
     sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
     results = sp.search(q=f'{query}', limit=1)
     for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        print(querytrack)
        queryartist = track["artists"][0]["name"]	
     embed=hikari.Embed(title="**Queued Track**",color=0x6100FF)
     try:
        embed.add_field(name="Name", value=f"{[querytrack]}({track['external_urls']['spotify']})", inline=False)
     except:
        embed.add_field(name="Name", value=f"{query_information.tracks[0].info.title}", inline=False)
     try:
        embed.add_field(name="Artist", value=f"{[queryartist]}({track['artists'][0]['external_urls']['spotify']})", inline=False)
     except:
        embed.add_field(name="Artist", value=f"{query_information.tracks[0].info.author}", inline=False)
     try:
        embed.add_field(name="Album", value=f"{[track['album']['name']]}({track['album']['external_urls']['spotify']})", inline=False)
     except:
        pass
     try:
        length = divmod(query_information.tracks[0].info.length, 60000)
        embed.add_field(name="Duration", value=f"{int(length[0])}:{round(length[1]/1000):02}")
     except:
        pass
     try:
        embed.add_field(name="Release Date", value=f"{track['album']['release_date']}", inline=False)
     except:
        pass
     try:
        embed.set_thumbnail(f"{track['album']['images'][0]['url']}")
     except:
        pass
     await ctx.respond(embed=embed)
    try:
        await music_plugin.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
    except lavasnek_rs.NoSessionPresent:
        pass

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("stop", "stops the currently playing song. (Type skip if you would like to move onto the next song.)", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def stop(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    results = sp.search(q=f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}", limit=1)
    print(f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}")  
    for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]	
    embed = hikari.Embed(title=f"**Stopped {node.now_playing.track.info.title}.**", colour=0x6100FF)
    try:
        embed.set_thumbnail(f"{track['album']['images'][0]['url']}")
    except:
        pass
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played", value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}")
    except:
        pass
    await music_plugin.d.lavalink.stop(ctx.guild_id)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("percentage", "What to change the volume to.", int , max_value=200 )
@lightbulb.command("volume", "Change the volume.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
@filament.utils.pass_options
async def volume(ctx: lightbulb.Context, percentage) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    await music_plugin.d.lavalink.volume(ctx.guild_id, int(percentage))
    embed=hikari.Embed(title=f"**Volume is now at {percentage}%**", color=0x6100FF)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("time", "What time you would like to seek to.", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("seek", "Seek to a specific point in a song.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
@filament.utils.pass_options
async def seek(ctx: lightbulb.Context, time) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    if not (match := re.match(TIME_REGEX, time)):
            embed = hikari.Embed(title="**Invalid time entered.**", colour=0xC80000)
            await ctx.respond(embed=embed)
    if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
    else:
            secs = int(match.group(1))
    await music_plugin.d.lavalink.seek_millis(ctx.guild_id, secs * 1000)
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    results = sp.search(q=f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}", limit=1)
    print(f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}")  
    for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]	
    embed = hikari.Embed(title=f"**Seeked {node.now_playing.track.info.title}.**", colour=0x6100FF)
    try:
        embed.set_thumbnail(f"{track['album']['images'][0]['url']}")
    except:
        pass
    try:
        length = divmod(node.now_playing.track.info.length, 60000)

        embed.add_field(name="Current Position", value=f"{time}/{int(length[0])}:{round(length[1]/1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("replay", "Replays the current song.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def replay(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    await music_plugin.d.lavalink.seek_millis(ctx.guild_id, 0000)
    embed = hikari.Embed(title=f"**Replaying {node.now_playing.track.info.title}.**", colour=0x6100FF)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("skip", "skips to the next song (if any).", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def skip(ctx: lightbulb.Context) -> None:
    skip = await music_plugin.d.lavalink.skip(ctx.guild_id)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    if not skip:
        embed = hikari.Embed(title="**There are no more tracks left in the queue.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    else:
        if not node.queue and not node.now_playing:
            await music_plugin.d.lavalink.stop(ctx.guild_id)
    embed = hikari.Embed(title=f"**Skipped {skip.track.info.title}.**", colour=0x6100FF)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("pause", "Pauses the currently playing track.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def pause(ctx: lightbulb.Context) -> None:
    await music_plugin.d.lavalink.pause(ctx.guild_id)
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    results = sp.search(q=f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}", limit=1)
    print(f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}")  
    for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]	
    embed = hikari.Embed(title=f"**Paused {node.now_playing.track.info.title}.**", colour=0x6100FF)
    try:
        embed.set_thumbnail(f"{track['album']['images'][0]['url']}")
    except:
        pass
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played", value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("resume", "Resumes playing the currently playing track.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def resume(ctx: lightbulb.Context) -> None:
    await music_plugin.d.lavalink.resume(ctx.guild_id)
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    results = sp.search(q=f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}", limit=1)
    print(f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}")  
    for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]	
    embed = hikari.Embed(title=f"**Resumed {node.now_playing.track.info.title}.**", colour=0x6100FF)
    try:
        embed.set_thumbnail(f"{track['album']['images'][0]['url']}")
    except:
        pass
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played", value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}")
    except:
        pass
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("nowplaying", "See what's currently playing.", auto_defer=True, aliases=["np","playing"])
@lightbulb.implements(lightbulb.SlashCommand)
async def now_playing(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    results = sp.search(q=f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}", limit=1)
    print(f"{node.now_playing.track.info.author} {node.now_playing.track.info.title}")  
    for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]	
    embed=hikari.Embed(title="**Currently Playing**",color=0x6100FF)
    try:
        embed.add_field(name="Name", value=f"{[querytrack]}({track['external_urls']['spotify']})", inline=False)
    except:
        embed.add_field(name="Name", value=f"{node.now_playing.track.info.title}", inline=False)
    try:
        embed.add_field(name="Artist", value=f"{[queryartist]}({track['artists'][0]['external_urls']['spotify']})", inline=False)
    except:
        embed.add_field(name="Artist", value=f"{node.now_playing.track.info.author}", inline=False)
    try:
        embed.add_field(name="Album", value=f"{[track['album']['name']]}({track['album']['external_urls']['spotify']})", inline=False)
    except:
        pass
    try:
        length = divmod(node.now_playing.track.info.length, 60000)
        position = divmod(node.now_playing.track.info.position, 60000)
        embed.add_field(name="Duration Played", value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}")
    except:
        pass
    try:
        embed.add_field(name="Release Date", value=f"{track['album']['release_date']}", inline=False)
    except:
        pass
    try:
        embed.set_thumbnail(f"{track['album']['images'][0]['url']}")
    except:
        pass
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("queue", "Shows you the queue.")
@lightbulb.implements(lightbulb.SlashCommand)
async def queue(ctx: lightbulb.Context) -> None:
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    if len(node.queue) == 1:
        embed = hikari.Embed(title="**The queue is currently empty.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    songs = [f'{tq.track.info.title} - {tq.track.info.author} ({int(divmod(tq.track.info.length, 60000)[0])}:{round(divmod(tq.track.info.length, 60000)[1]/1000):02})' for i, tq in enumerate(node.queue[1:], start=1)]
    chunks = [songs[i : i + 10] for i in range(0, len(songs), 10)]
    embeds = []
    i = 1
    for chunk in chunks:
        texts = []
        for track in chunk:
            texts.append(f"**{i}.** {track}")
            i += 1
        names = "\n".join(texts)
        songs = hikari.Embed(title="**The Queue**", description=names, color=0x6100FF)
        embeds.append(songs)
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    results = sp.search(q=f'{node.queue[1].track.info.author} {node.queue[1].track.info.title}', limit=1)
    for idx, track in enumerate(results['tracks']['items']):
        querytrack = track['name']
        queryartist = track["artists"][0]["name"]	
    try:
        songs.set_thumbnail(f"{track['album']['images'][0]['url']}")
    except:
        pass
    navigator = nav.NavigatorView(pages=embeds)
    await navigator.send(ctx.interaction)
    
@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("index", "Index for the song you want to remove.", int, required = True)
@lightbulb.command("remove", "Removes a song from the queue.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def remove(ctx: lightbulb.Context, index) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
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
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("position", "The song's position in the queue.", int, required = True)
@lightbulb.command("skipto", "skip to a different song in the queue.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def skipto(ctx: lightbulb.Context, position) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    index = position
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if index == 0:
        embed = hikari.Embed(title=f"**You cannot move to a song that is currently playing.**",color=0xC80000)
        return await ctx.respond(embed=embed)
    if index == 1:
        embed = hikari.Embed(title=f"**Skipping to the next song.**",color=0xC80000)
        await music_plugin.d.lavalink.skip(ctx.guild_id)
        return await ctx.respond(embed=embed)
    try:
     queue = node.queue
     song_to_be_skipped = queue[index]
    except:
        embed = hikari.Embed(title=f"**Incorrect position entered.**",color=0xC80000)
        return await ctx.respond(embed=embed)
    queue.insert(1, queue[index])
    queue.pop(index)
    queue.pop(index)
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    await music_plugin.d.lavalink.skip(ctx.guild_id)
    embed = hikari.Embed(title=f"**Skipped to {song_to_be_skipped.track.info.title}.**",color=0x6100FF)
    await ctx.respond(embed=embed)
    
@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("loop", "Loops the currently playing song!", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def loop(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return None
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    loop_enabled = node.get_data().get("loop")
    if loop_enabled:
        node.set_data({"loop": False})
        embed = hikari.Embed(title="**Disabled the loop.**", color=0x6100FF)
        await ctx.respond(embed=embed)
    else:
        node.set_data({"loop": True})
        embed = hikari.Embed(title="**Enabled the loop.**", color=0x6100FF)
        await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("current_position", "The song's current position in the queue.", int, required = True)
@lightbulb.option("new_position", "The song's new position in the queue.", int, required = True)
@lightbulb.command("move", "Move a song to a different position in the queue.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def move(ctx: lightbulb.Context, current_position, new_position) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        await ctx.respond(embed=embed)
        return
    new_index = new_position
    old_index = current_position
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not len(node.queue) >= 1:
        embed = hikari.Embed(title=f"**There is only 1 song in the queue.**",color=0xC80000)
        return await ctx.respond(embed=embed)
    queue = node.queue
    song_to_be_moved = queue[old_index]
    try:
        queue.pop(old_index)
        queue.insert(new_index, song_to_be_moved)
    except:
        embed = hikari.Embed(title=f"**Incorrect position entered.**",color=0xC80000)
        return await ctx.respond(embed=embed)
    node.queue = queue
    await music_plugin.d.lavalink.set_guild_node(ctx.guild_id, node)
    embed = hikari.Embed(title=f"**Moved {song_to_be_moved.track.info.title} to position {new_index}.**", color=0x6100FF)
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("empty", "Clear the queue.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def empty(ctx: lightbulb.Context) -> None:
    states = music_plugin.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        embed = hikari.Embed(title="**You are not in a voice channel.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.now_playing:
        embed = hikari.Embed(title="**There are no songs playing at the moment.**", colour=0xC80000)
        return await ctx.respond(embed=embed)
    node = await music_plugin.d.lavalink.get_guild_node(ctx.guild_id)
    await music_plugin.d.lavalink.stop(ctx.guild_id)
    await music_plugin.d.lavalink.leave(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_node(ctx.guild_id)
    await music_plugin.d.lavalink.remove_guild_from_loops(ctx.guild_id)
    await music_plugin.bot.update_voice_state(ctx.guild_id, None)
    await music_plugin.d.lavalink.wait_for_connection_info_remove(ctx.guild_id)
    await _join(ctx)
    embed=hikari.Embed(title="**Emptied the queue.**",color=0x6100FF)
    await ctx.respond(embed=embed)
    
@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("newreleases", "See the latest releases for the day.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def newreleases(ctx: lightbulb.Context) -> None:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    response = sp.new_releases(limit=21)
    albums = response['albums']
    today = date.today()
    embed=hikari.Embed(title=f"**New Releases - {today}**", color=0x6100FF)
    embed.add_field(name="Latest Tracks", value=f"\n".join([f"**{i}.** {item['name']}" for i, item in enumerate(albums['items'][1:], start=1)]))
    img = response['albums']['items'][1]['images'][0]['url']
    try:
      embed.set_thumbnail(img)
    except:
        pass
    await ctx.respond(embed=embed)

@music_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("trending", "See the latest trending tracks.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def trending(ctx: lightbulb.Context) -> None:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID,client_secret=SPOTCLIENT_SECRET))
    playlist_URI = "37i9dQZF1DXcBWIGoYBM5M"
    track_uris = [x["track"]["uri"] for x in sp.playlist_items(playlist_URI)["items"]]
    track = sp.track(track_uris[1])
    today = date.today()
    embed=hikari.Embed(title=f"**Trending Tracks - {today}**", color=0x6100FF)
    embed.add_field(name="Top 20 Tracks Of The Day", value=f"\n".join([f"**{i}.** {track['track']['name']}" for i, track in enumerate(sp.playlist_items(playlist_URI, limit=21)["items"][1:], start=1)]))
    img = track['album']['images'][0]['url']
    try:
      embed.set_thumbnail(img)
    except:
        pass
    await ctx.respond(embed=embed)

if HIKARI_VOICE:

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
    miru.load(bot)
    bot.add_plugin(music_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(music_plugin)
