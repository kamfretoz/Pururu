import lightbulb
import hikari
import time
import datetime

ping_plugin = lightbulb.Plugin("ping")

@ping_plugin.command()
@lightbulb.command("ping", "measure the ping of the bot", ephemeral = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    start = time.monotonic()
        
    millis = (time.monotonic() - start) * 1000
    heartbeat = ctx.bot.heartbeat_latency * 1000
    
    if heartbeat > 1000:
        colours = hikari.Colour(0xFF0000)
    elif heartbeat > 500:
        colours = hikari.Colour(0xFFFF00)
    else:
        colours = hikari.Colour(0x26D934)
    
    ping = hikari.Embed(
            title="Current Ping:",
            description=f"```💓: {heartbeat:,.2f}ms.```",
            timestamp=datetime.datetime.now().astimezone(),
            color=colours,
        )
    await ctx.respond(embed=ping)
    
    
def load(bot):
    bot.add_plugin(ping_plugin)

def unload(bot):
    bot.remove_plugin(ping_plugin)