import lightbulb
import hikari
import json
import dotenv
import os
from datetime import datetime

curr_plugin = lightbulb.Plugin("currency")

# To retrieve KSoft.Si API KEY
dotenv.load_dotenv()
ksoft_key = os.environ.get("KSOFT_API_KEY")

@curr_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("value", "The amount you want to convert", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("to", "The currency you want to convert to", hikari.OptionType.STRING, required=True)
@lightbulb.option("origin", "The currency you want to convert from", hikari.OptionType.STRING, required=True)
@lightbulb.command("currency", "Convert value from one currency to another", aliases=["curr"], auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def currency(ctx: lightbulb.Context) -> None:
    origin = ctx.options.origin
    to = ctx.options.to
    val = ctx.options.value
    
    head = {
        "Authorization": ksoft_key
    }
    params = {
        "from": origin,
        "to": to,
        "value": val
    }
    async with ctx.bot.d.aio_session.get('https://api.ksoft.si/kumo/currency', headers=head, params=params) as resp:
        data = json.loads(await resp.read())
    try:
        prt = data["pretty"]
    except KeyError:
        code = data["code"]
        msg = data["message"]
        raise ValueError(f"⚠ An Error Occured! **{msg.capitalize()}** (Code: {code})")

    emb = hikari.Embed(timestamp=datetime.now().astimezone())
    emb.add_field(
        name=f"Conversion from {origin.upper()} to {to.upper()}", value=prt)
    emb.set_footer("Data provided by: KSoft.Si")
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(curr_plugin)

def unload(bot):
    bot.remove_plugin(curr_plugin)
