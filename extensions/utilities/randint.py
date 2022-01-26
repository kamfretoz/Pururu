import lightbulb
import hikari
import random

randint_plugin = lightbulb.Plugin("randint")

@randint_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("end", "The start of the range", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("begin", "The start of the range", hikari.OptionType.INTEGER, required=True)
@lightbulb.command("randint", "Give you a randomized number between a range", aliases=["randnum"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def randint(ctx: lightbulb.Context) -> None:
    a = ctx.options.begin
    b = ctx.options.end
    
    if b > a or a < b:
        em = hikari.Embed(color=0x00ff00, title='Your randomized number:')
        em.description = random.randint(a, b)
        await ctx.respond(embed=em)
    else:
        raise ValueError("The end range cannot be smaller than the begin range")

def load(bot):
    bot.add_plugin(randint_plugin)

def unload(bot):
    bot.remove_plugin(randint_plugin)
