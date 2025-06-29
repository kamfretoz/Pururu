import hikari
import lightbulb
from zoneinfo import ZoneInfo, available_timezones
from datetime import datetime
from rapidfuzz import fuzz, process
from functools import lru_cache

@lru_cache(maxsize=100)
def get_timezones():
    return available_timezones()

loader = lightbulb.Loader()

async def timezone_autocomplete(ctx: lightbulb.AutocompleteContext[str]):
    result = process.extract(ctx.focused.value, get_timezones(), scorer=fuzz.QRatio, limit=5)
    
    if len(result) == 0:
        await ctx.respond("Could not find anything. Sorry.")
    
    await ctx.respond([r[0] for r in result])

@loader.command
class Clock(
    lightbulb.SlashCommand, name="clock", description="View current time and date"
):
    timezone = lightbulb.string("timezone", "The timezone you want to look up!", str, required=False, autocomplete=timezone_autocomplete, default="UTC")

    @lightbulb.invoke
    async def invoke(
        self, ctx: lightbulb.Context
    ) -> None:

        time = datetime.now(ZoneInfo(self.timezone))
        time_fmt = time.strftime("%I:%M:%S %p")
        date_fmt = time.strftime("%A, %d %B %Y")

        clock = hikari.Embed(color=0xC0C0C0)
        clock.add_field(name="🕓 Current Time", value=time_fmt, inline=False)
        clock.add_field(name="📆 Current Date", value=date_fmt, inline=False)
        clock.add_field(name="🌐 Timezone", value=self.timezone, inline=False)
        await ctx.respond(embed=clock, content="⏰ Tick.. Tock..")