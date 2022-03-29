import lightbulb
import hikari
import json
from utils.time import format_seconds

anifinder_plugin = lightbulb.Plugin("animefinder", "Anime Lookup with screenshot leveraging https://trace.moe/")

@anifinder_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("image", "The image you want to lookup", hikari.Attachment, required=True)
@lightbulb.command("anifinder", "Find anime by screenshot", auto_defer=True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def anifinder(ctx: lightbulb.Context, image: hikari.Attachment) -> None:
    # First we get the image from the attachment
    attachment = image.url
    
    # Then we send the image to the API
    parameters = {
        "url" : attachment
    }
    async with ctx.bot.d.aio_session.get("https://api.trace.moe/search?cutBorders", params = parameters) as resp:
        data = json.loads(await resp.read())
    
    # Then we parse the response from the API
    try:
        anilist = data["result"][0]["anilist"]
        filename = data["result"][0]["filename"]
        episode = data["result"][0]["episode"]
        start = data["result"][0]["from"]
        end = data["result"][0]["to"]
        similarity = data["result"][0]["similarity"]
        thumb = data["result"][0]["image"]
    except:
        await ctx.respond(embed=hikari.Embed(description="⚠ An Error occured while parsing the data, Please try again later."))
        return
    
    emb = hikari.Embed(title="Anime Finder")
    emb.add_field(name="AniList ID", value=anilist)
    emb.add_field(name="File Name", value=filename, inline=False)
    emb.add_field(name="Episode Number", value=episode or "Unknown")
    emb.add_field(name="Start", value=format_seconds(start))
    emb.add_field(name="End", value=format_seconds(end))
    emb.add_field(name="Similarity Score", value=similarity)
    emb.set_image(hikari.URL(thumb))
    
    # Then we send the result
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(anifinder_plugin)

def unload(bot):
    bot.remove_plugin(anifinder_plugin)
