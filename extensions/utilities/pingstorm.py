import lightbulb
import hikari
import asyncio

pingstorm_plugin = lightbulb.Plugin("pingstorm", "ping deez nuts", include_datastore = True)
pingstorm_plugin.d.lock = asyncio.Lock()

@pingstorm_plugin.command()
@lightbulb.add_cooldown(3600, 2, lightbulb.cooldowns.GuildBucket)
@lightbulb.option("amount", "The amount of the pings", int, required = False, default=5, min_value=1, max_value=100)
@lightbulb.option("user", "The target user", hikari.Member, required = True)
@lightbulb.command("pingstorm", "Ping specified user number of times", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def pingstorm(ctx: lightbulb.Context) -> None:
    amount = ctx.options.amount
    user = ctx.options.user
    if amount > 100:
        await ctx.respond("**WARNING:** **Maximum allowed amount is 100.**")
        return
    if user.id == ctx.bot.application.id:
        await ctx.respond("HA! You think it'll work against me?? Nice Try.")
        user = ctx.author
        await asyncio.sleep(2)
    if not pingstorm_plugin.d.lock.locked():
        async with pingstorm_plugin.d.lock:
            await ctx.respond("Ping Machine Initializing in 3 seconds!")                
            await asyncio.sleep(3)
            await ctx.respond("Begin!")
            ping = 0
            while ping < int(amount):
                await ctx.respond(f"{user.mention} - {ping + 1}/{amount}")
                ping += 1
                await asyncio.sleep(0.5)
            await ctx.respond("Finished!")
            await ctx.delete_last_response()


def load(bot):
    bot.add_plugin(pingstorm_plugin)

def unload(bot):
    bot.remove_plugin(pingstorm_plugin)
