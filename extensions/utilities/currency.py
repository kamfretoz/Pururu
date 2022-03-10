import lightbulb
import hikari
import json
import dotenv
import os
from datetime import datetime
from lightbulb.ext import filament

curr_plugin = lightbulb.Plugin("currency", "money money money")

dotenv.load_dotenv()
curr_key = os.environ["GEO_CURR_API"]

@curr_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("val", "The amount you want to convert", int, required=True)
@lightbulb.option("to", "The currency you want to convert to", str, required=True)
@lightbulb.option("origin", "The currency you want to convert from", str, required=True)
@lightbulb.command("currency", "Convert value from one currency to another", aliases=["curr"], auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def currency(ctx: lightbulb.Context, origin: str, to: str, val: int):
    parameters = {
        "api_key": curr_key,
        "from": origin,
        "to": to,
        "amount": val,
    }
    async with ctx.bot.d.aio_session.get('https://api.getgeoapi.com/v2/currency/convert', params=parameters) as resp:
        data = json.loads(await resp.read())


    if data["status"] == "success":
        origin_name = data["base_currency_name"]
        to_name = data["rates"][to.upper()]["currency_name"]
        to_amount = data["rates"][to.upper()]["rate_for_amount"]
    elif data["status"] == "failed":
        err = data["error"]["message"]
        code = data["error"]["code"]
        return await ctx.respond(f"Error! {err} ({code})")
    else:
        await ctx.respond("Unable to parse the data! something is wrong...")

    emb = hikari.Embed(timestamp=datetime.now().astimezone())
    emb.add_field(
        name=f"Conversion from {val} {origin_name} to {to_name}", value=f"{to_amount} {to_name}"
        )
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(curr_plugin)

def unload(bot):
    bot.remove_plugin(curr_plugin)
