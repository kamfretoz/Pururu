import lightbulb
import hikari
import datetime

ping_plugin = lightbulb.Plugin("ping")

@ping_plugin.command()
@lightbulb.command("ping", "measure the ping of the bot", ephemeral = True, auto_defer=True, aliases=["pong"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    heartbeat = ctx.bot.heartbeat_latency * 1000
    
    if isinstance(ctx, lightbulb.PrefixContext):
        if ctx.invoked_with == "pong":
            txt = (f":ping_pong: Ping!")
        else:
            txt = (f":ping_pong: Pong!")
    
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
    await ctx.respond(embed=ping, content=txt)
    
    
def load(bot):
    bot.add_plugin(ping_plugin)

def unload(bot):
    bot.remove_plugin(ping_plugin)
