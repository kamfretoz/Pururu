import lightbulb
import hikari
import random
from lightbulb.ext import filament

randint_plugin = lightbulb.Plugin("randint", "Gimme random number!")

@randint_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("end", "The start of the range", int, required=True, default=420)
@lightbulb.option("begin", "The start of the range", int, required=True, default=69)
@lightbulb.command("randint", "Give you a randomized number between a range", aliases=["randnum"], auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def randint(ctx: lightbulb.Context, begin, end) -> None:
    if end > begin or begin < end:
        em = hikari.Embed(color=0x00ff00, title='Your randomized number:')
        em.description = random.randint(begin, end)
        await ctx.respond(embed=em)
    else:
        raise ValueError("The end range cannot be smaller than the begin range")

def load(bot):
    bot.add_plugin(randint_plugin)

def unload(bot):
    bot.remove_plugin(randint_plugin)
