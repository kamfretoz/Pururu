import lightbulb
import hikari
import json
import ciso8601
import asyncio
from datetime import datetime
from textwrap import shorten

mal_plugin = lightbulb.Plugin("myanimelist")

@mal_plugin.command()
@lightbulb.option("name", "The anime you want to lookup", hikari.OptionType.STRING, required=True)
@lightbulb.command("anime", "Find the information of an Anime", aliases=["mal"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def myanime(ctx: lightbulb.Context) -> None:
    name = ctx.options.name
    parameters = {
        "q": name,
        "limit": 1
    }
    try:
        async with ctx.bot.d.aio_session.get('https://api.jikan.moe/v3/search/anime', params=parameters, timeout=10) as resp:
            data = json.loads(await resp.read())
    except asyncio.exceptions.TimeoutError:
        raise ValueError("⚠ A Timeout Error occured, please try again!")
    try:
        anime_id = data["results"][0]["mal_id"]
        anime_title = data["results"][0]["title"]
        anime_url = data["results"][0]["url"]
        anime_img = data["results"][0]["image_url"]
        anime_status = data["results"][0]["airing"]
        anime_synopsis = data["results"][0]["synopsis"]
        anime_type = data["results"][0]["type"]
        score = data["results"][0]["score"]
    except KeyError:
        raise ValueError("⚠ Result not found, maybe check your input?")

    emb = hikari.Embed(
        title="MyAnimeList Anime Information", timestamp=datetime.now().astimezone())
    if score == None or score == 0:
        score = "N/A"
    start = data["results"][0]["start_date"]
    end = data["results"][0]["end_date"]
    mem = data["results"][0]["members"]
    # Time zone converter (a few checks will depends on the presence of time_end value)
    try:
        time_start = ciso8601.parse_datetime(start)
        formatted_start = time_start.strftime("%B %d, %Y")
    except TypeError:
        formatted_start = "Unknown"
    try:
        time_end = ciso8601.parse_datetime(end)
        formatted_end = time_end.strftime("%B %d, %Y")
    except TypeError:
        formatted_end = "Unknown"
    try:
        total_episode = data["results"][0]["episodes"]
        if total_episode == 0 or total_episode is None:
            total_episode = "Not yet determined"
    except TypeError:
        total_episode = "Not yet determined."
    if anime_status:
        anime_status = "Ongoing"
    elif not anime_status:
        if start is None:
            anime_status = "Not yet aired"
        else:
            anime_status = "Finished airing"
    if len(anime_synopsis) > 1024:
        shorten(anime_synopsis,width=1020,placeholder="...")
    emb.set_image(anime_img)
    emb.set_thumbnail("https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
    emb.set_footer("Powered by: Jikan")
    emb.add_field(name="📝 Title",value=f"[{anime_title}]({anime_url})", inline=False)
    if anime_synopsis:
        emb.add_field(name="ℹ Synopsis",value=anime_synopsis, inline=False)
    else:
        emb.add_field(name="ℹ Synopsis",value="No Synopsis Found.", inline=False)
    emb.add_field(name="⌛ Status", value=anime_status, inline=False)
    emb.add_field(name="📺 Type", value=anime_type, inline=False)
    emb.add_field(name="📅 First Air Date",value=formatted_start, inline=False)
    emb.add_field(name="📅 Last Air Date",value=formatted_end, inline=False)
    emb.add_field(name="💿 Episodes", value=total_episode, inline=True)
    emb.add_field(name="⭐ Score", value=f"{score}", inline=True)
    try:
        rate = data["results"][0]["rated"]
        if rate is None:
            rating = "Unknown"
        else:
            rating = {
                'G': 'All Ages (G)',
                'PG': 'Children (PG)',
                'PG-13': 'Teens 13 or Older (PG-13)',
                'R': '17+ Recommended, (Violence & Profanity) (R)',
                'R+': 'Mild Nudity, (May also contain Violence & Profanity) (R+)',
                'Rx': 'Hentai, (Extreme sexual content/Nudity) (Rx)'
            }.get(str(rate))
        emb.add_field(name="🔞 Rating", value=rating, inline=True)
    except IndexError:
        pass
    except AttributeError:
        pass
    except KeyError:
        pass
    emb.add_field(name="👥 Members", value=mem, inline=True)
    emb.add_field(name="💳 ID", value=anime_id, inline=True)
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(mal_plugin)

def unload(bot):
    bot.remove_plugin(mal_plugin)
