import lightbulb
import hikari
import json
import dotenv
import os
from datetime import datetime


wikihow_plugin = lightbulb.Plugin("wikihow", "wikihow yes")

# To retrieve KSoft.Si API KEY
dotenv.load_dotenv()
ksoft_key = os.environ.get("KSOFT_API_KEY")

@wikihow_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.command("wikihow", "Sends a random weird imagery from wikihow", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def wikihow(ctx: lightbulb.Context):
    head = {
        "Authorization": ksoft_key
    }
    param = {
        "nsfw": "false"
    }
    async with ctx.bot.d.aio_session.get('https://api.ksoft.si/images/random-wikihow', headers=head, params=param) as resp:
        data = json.loads(await resp.read())
    try:
        img_url = data["url"]
        title = data["title"]
        article = data["article_url"]
    except KeyError:
        code = data["code"]
        msg = data["message"]
        raise ValueError(f"⚠ An Error Occured! {msg.capitalize()} (Code: {code})")
    emb = hikari.Embed(
        description=f"[{title}]({article})", timestamp=datetime.now().astimezone())
    emb.set_image(img_url)
    emb.set_footer("Data provided by: KSoft.Si" , icon="https://cdn.ksoft.si/images/Logo128.png")
    await ctx.respond(embed=emb)


def load(bot):
    bot.add_plugin(wikihow_plugin)

def unload(bot):
    bot.remove_plugin(wikihow_plugin)
