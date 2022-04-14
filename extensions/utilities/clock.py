import hikari
import lightbulb
from zoneinfo import ZoneInfo, available_timezones
from datetime import datetime
from rapidfuzz import fuzz, process
from functools import lru_cache

@lru_cache(maxsize=100)
def get_timezones():
    return available_timezones()

clock_plugin = lightbulb.Plugin("clock", "Time related commands")

@clock_plugin.command
@lightbulb.option("timezone", "The timezone you want to look up!", str, required=False, autocomplete=True)
@lightbulb.command("clock", "Lookup the time on a certain timezone!", aliases=["time"], pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def clock(ctx: lightbulb.Context, timezone: str):
    if not timezone:
        timezone = "UTC"
    
    time = datetime.now(ZoneInfo(timezone))
    time_fmt = time.strftime("%I:%M:%S %p")
    date_fmt = time.strftime("%A, %d %B %Y")
    
    clock = hikari.Embed(color=0xC0C0C0)
    clock.add_field(name="🕓 Current Time", value=time_fmt, inline=False)
    clock.add_field(name="📆 Current Date", value=date_fmt, inline=False)
    clock.add_field(name="🌐 Timezone", value=timezone, inline=False)
    await ctx.respond(embed=clock, content=f"⏰ Tick.. Tock..")
    
@clock.autocomplete("timezone")
async def timezone_autocomplete(input: hikari.AutocompleteInteractionOption, interaction: hikari.AutocompleteInteraction):
    result = process.extract(input.value, get_timezones(), scorer=fuzz.QRatio, limit=5)
    
    if len(result) == 0:
        return "Could not find anything. Sorry."
    
    return [r[0] for r in result]

def load(bot):
    bot.add_plugin(clock_plugin)

def unload(bot):
    bot.remove_plugin(clock_plugin)