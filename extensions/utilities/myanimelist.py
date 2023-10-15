import lightbulb
import hikari
import json
import ciso8601
import asyncio
from datetime import datetime
from textwrap import shorten

mal_plugin = lightbulb.Plugin("myanimelist", "Weebs Only")

@mal_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("name", "The anime you want to lookup", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("anime", "Find the information of an Anime", aliases=["ani"], auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def myanimelist_anime(ctx: lightbulb.Context, name: str) -> None:
    parameters = {
        "q": name,
        "limit": 1,
        "page": 1,
        "sort": "asc",
    }
    try:
        async with ctx.bot.d.aio_session.get('https://api.jikan.moe/v4/anime', params=parameters, timeout=10) as resp:
            data = json.loads(await resp.read())
    except asyncio.exceptions.TimeoutError:
        raise ValueError("⚠ A Timeout Error occured, please try again!")
    
    if not data["data"]:
        raise ValueError("⚠ No result found.")

    anime_id = data["data"][0]["mal_id"]
    anime_title = data["data"][0]["title"]
    anime_url = data["data"][0]["url"]
    anime_img = data["data"][0]["images"]["webp"]["large_image_url"]
    anime_status = data["data"][0]["status"]
    anime_synopsis = data["data"][0]["synopsis"]
    anime_type = data["data"][0]["type"]
    score = data["data"][0]["score"]

    emb = hikari.Embed(
        title="MyAnimeList Anime Information", timestamp=datetime.now().astimezone(), url="https://www.myanimelist.net")
    if score == None or score == 0:
        score = "N/A"
    start = data["data"][0]["aired"]["from"]
    end = data["data"][0]["aired"]["to"]
    mem = data["data"][0]["members"]
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
        total_episode = data["data"][0]["episodes"]
        if total_episode == 0 or total_episode is None:
            total_episode = "Not yet determined"
    except TypeError:
        total_episode = "Not yet determined."
    emb.set_image(anime_img)
    emb.set_thumbnail("https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
    emb.set_footer("Powered by: Jikan", icon="https://jikan.moe/assets/images/logo/jikan.logo.png")
    emb.add_field(name="📝 Title",value=f"[{anime_title}]({anime_url})", inline=False)
    if anime_synopsis:
        synopsis = anime_synopsis
        if len(anime_synopsis) > 1024:
            synopsis = shorten(anime_synopsis,width=1000,placeholder="...")
        emb.add_field(name="ℹ Synopsis",value=synopsis, inline=False)
    else:
        emb.add_field(name="ℹ Synopsis",value="No Synopsis Found.", inline=False)
    emb.add_field(name="⌛ Status", value=anime_status, inline=False)
    emb.add_field(name="📺 Type", value=anime_type, inline=False)
    emb.add_field(name="📅 First Air Date",value=formatted_start, inline=False)
    emb.add_field(name="📅 Last Air Date",value=formatted_end, inline=False)
    emb.add_field(name="💿 Episodes", value=total_episode, inline=True)
    emb.add_field(name="⭐ Score", value=f"{score}", inline=True)
    try:
        rating = data["data"][0]["rating"]
        if rating is None:
            rating = "Unknown"
        emb.add_field(name="🔞 Rating", value=rating, inline=True)
    except IndexError:
        pass
    emb.add_field(name="👥 Members", value=mem, inline=True)
    emb.add_field(name="💳 ID", value=anime_id, inline=True)
    await ctx.respond(embed=emb)
    
@mal_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("name", "The manga you want to lookup", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("manga", "Find the information of a manga", aliases=["man"], auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def myanimelist_manga(ctx: lightbulb.Context, name: str, sfw: bool):
    parameters = {
        "q": name,
        "limit": 1,
        "page": 1,
        "sort": "asc",
    }
    try:
        async with ctx.bot.d.aio_session.get(f'https://api.jikan.moe/v4/manga', params=parameters, timeout=10) as resp:
            data = json.loads(await resp.read())
    except asyncio.exceptions.TimeoutError:
        raise ValueError("⚠ A Timeout Error occured, please try again!")
    
    if not data["data"]:
        raise ValueError("⚠ No result found.")
    
    manga_title = data["data"][0]["title"]
    manga_url = data["data"][0]["url"]
    img_url = data["data"][0]["images"]["webp"]["large_image_url"]
    stat = data["data"][0]["status"]
    manga_synopsis = data["data"][0]["synopsis"]
    manga_type = data["data"][0]["type"]
    manga_chapters = data["data"][0]["chapters"]
    manga_volumes = data["data"][0]["volumes"]
    score = data["data"][0]["scored"]
    pub_date = data["data"][0]["published"]["from"]
    memb = data["data"][0]["members"]
    manga_id = data["data"][0]["mal_id"]
    time_start = ciso8601.parse_datetime(pub_date)
    formatted_start = time_start.strftime("%B %d, %Y")
    
    if manga_volumes is None or manga_volumes == 0:
        manga_volumes = "Unknown"
    if manga_chapters is None or manga_chapters == 0:
        manga_chapters = "Unknown"
    emb = hikari.Embed(
        title="MyAnimeList Manga Information", timestamp=datetime.now().astimezone(), url="https://www.myanimelist.net")
    emb.set_image(img_url)
    emb.set_thumbnail("https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
    emb.set_footer("Powered by: Jikan", icon="https://jikan.moe/assets/images/logo/jikan.logo.png")
    emb.add_field(name="📑 Title",value=f"[{manga_title}]({manga_url})", inline=False)
    if manga_synopsis:
        synopsis = manga_synopsis
        if len(manga_synopsis) > 1024:
            synopsis = shorten(manga_synopsis,width=1000,placeholder="...")
        emb.add_field(name="ℹ Synopsis",value=synopsis, inline=False)
    else:
        emb.add_field(name="ℹ Synopsis",value="No Synopsis Found.", inline=False)
    emb.add_field(name="⏳ Status", value=stat, inline=False)
    emb.add_field(name="📁 Type", value=manga_type, inline=False)
    emb.add_field(name="📅 Publish Date",value=formatted_start, inline=False)
    emb.add_field(name="📚 Volumes", value=manga_volumes, inline=True)
    emb.add_field(name="📰 Chapters", value=manga_chapters, inline=True)
    emb.add_field(name="⭐ Score", value=f"{score}", inline=True)
    emb.add_field(name="👥 Members", value=memb, inline=True)
    emb.add_field(name="💳 ID", value=manga_id, inline=True)
    await ctx.respond(embed=emb)

@mal_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("name", "The character name you want to lookup", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("character", "Find the information of an anime character", aliases=["chara"], auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def myanimelist_chara(ctx: lightbulb.Context, name):
    parameters = {
        "q": name,
        "limit": 1
    }
    try:
        async with ctx.bot.d.aio_session.get(f'https://api.jikan.moe/v4/characters', params=parameters, timeout=10) as resp:
            data = json.loads(await resp.read())
    except asyncio.exceptions.TimeoutError:
        raise ValueError("⚠ A Timeout Error occured, please try again!")
    if not data["data"]:
        raise ValueError("⚠ No result found.")
    char_id = data["data"][0]["mal_id"]
    char_url = data["data"][0]["url"]
    char_img = data["data"][0]["images"]["webp"]["image_url"]
    char_name = data["data"][0]["name"]
    char_about = data["data"][0]["about"]
    
    emb = hikari.Embed(title="MyAnimeList Character Information", timestamp=datetime.now().astimezone(), url="https://www.myanimelist.net")
    emb.set_image(char_img)
    emb.set_thumbnail("https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png")
    emb.set_footer("Powered by: Jikan", icon="https://jikan.moe/assets/images/logo/jikan.logo.png")
    emb.add_field(name="👤 Name", value=f"[{char_name}]({char_url})", inline=False)
    try:
        char_nick = data["data"][0]["nicknames"][0]
        emb.add_field(name="👤 Nickname", value=f"{char_nick}", inline=False)
    except IndexError:
        pass

    if char_about:
        about = char_about
        if len(about) > 1024:
            about = shorten(char_about, width=1000,placeholder="...")
            emb.add_field(name="ℹ️ About", value=about, inline=False)

    emb.add_field(name="💳 ID", value=char_id, inline=True)
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(mal_plugin)

def unload(bot):
    bot.remove_plugin(mal_plugin)
