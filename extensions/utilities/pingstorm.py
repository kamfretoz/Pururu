import lightbulb
import hikari
import asyncio
from lightbulb.buckets import GuildBucket

pingstorm_plugin = lightbulb.Plugin("pingstorm", "ping deez nuts", include_datastore = True)

@pingstorm_plugin.command()
@lightbulb.add_cooldown(3600, 2, GuildBucket)
@lightbulb.set_max_concurrency(1, GuildBucket)
@lightbulb.option("amount", "The amount of the pings", int, required = False, default=5, min_value=1, max_value=100)
@lightbulb.option("user", "The target user", hikari.Member, required = True)
@lightbulb.command("pingstorm", "Ping specified user number of times", hidden=True, pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def pingstorm(ctx: lightbulb.Context, amount: int, user: hikari.Member) -> None:
    if amount > 100:
        await ctx.respond("**WARNING:** **Maximum allowed amount is 100.**")
        return
    if user.id == ctx.bot.application.id:
        await ctx.respond("HA! You think it'll work against me?? Nice Try.", delete_after=3)
        user = ctx.author
        await asyncio.sleep(2)
    await ctx.respond("Ping Machine Initializing in 3 seconds!", delete_after=5)                
    await asyncio.sleep(3)
    await ctx.respond("Begin!", delete_after=5)
    ping = 0
    for x in range(amount):
        await ctx.respond(f"{user.mention} - {ping + 1}/{amount}", delete_after=60, user_mentions=True)
        ping += 1
        await asyncio.sleep(3)
    await ctx.respond("Finished!", delete_after=5)


def load(bot):
    bot.add_plugin(pingstorm_plugin)

def unload(bot):
    bot.remove_plugin(pingstorm_plugin)
