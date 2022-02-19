import hikari
import lightbulb
import psutil
import platform
from datetime import datetime

stats_plugin = lightbulb.Plugin("stats", "Statistics of this bot", include_datastore = True)

stats_plugin.d.counter = datetime.now()

@stats_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.command("stats", "Get statistics info of the bot.", auto_defer = True, ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def stats(ctx: lightbulb.Context) -> None:
    """Bot stats."""

    def solveunit(input):
        output = ((input // 1024) // 1024) // 1024
        return int(output)

    try:
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().uss / 1024 ** 2
        )
    except AttributeError:
        # OS doesn't support retrieval of USS (probably BSD or Solaris)
        mem_usage = "{:.2f} MiB".format(
            __import__("psutil").Process(
            ).memory_full_info().rss / 1024 ** 2
        )
    sysboot = datetime.fromtimestamp(psutil.boot_time()).strftime("%B %d, %Y at %I:%M:%S %p")
    uptime = datetime.now() - stats_plugin.d.counter
    uptime = datetime.now() - stats_plugin.d.counter
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)
    days, hours = divmod(hours, 24)
    guilds = await ctx.bot.rest.fetch_my_guilds()
    
    if days:
        time = "%s days, %s hours, %s minutes, and %s seconds" % (
            days,
            hours,
            minutes,
            seconds,
        )
    else:
        time = "%s hours, %s minutes, and %s seconds" % (
            hours, minutes, seconds)
    em = hikari.Embed(title="System Status", color=0x32441C)
    em.add_field(
        name=":desktop: CPU Usage",
        value=f"{psutil.cpu_percent():.2f}% ({psutil.cpu_count(logical=False)} Cores / {psutil.cpu_count(logical=True)} Threads) \nload avg: {psutil.getloadavg()}",
        inline=False,
    )
    em.add_field(
        name=":computer: System Memory Usage",
        value=f"**{psutil.virtual_memory().percent}%** Used",
        inline=False,
    )
    em.add_field(
        name=":dna: Kernel Version",
        value=platform.platform(aliased=True, terse=True),
        inline=False,
    )
    em.add_field(
        name=":gear: Library version",
        value=f"hikari {hikari.__version__}",
        inline=False,
    )
    em.add_field(
        name="\U0001F4BE BOT Memory usage",
        value=mem_usage,
        inline=False
    )
    em.add_field(
        name=":minidisc: Disk Usage",
        value=f"Total Size: {solveunit(psutil.disk_usage('/').total)} GB \nCurrently Used: {solveunit(psutil.disk_usage('/').used)} GB",
        inline=False,
    )
    em.add_field(
        name="\U0001F553 BOT Uptime",
        value=time,
        inline=False
    )
    em.add_field(
        name="⏲️ Last System Boot Time",
        value=sysboot,
        inline=False
    )
    em.add_field(
        name="\u2694 Servers (Guilds)",
        value=str(len(guilds)),
        inline=False
    )
    await ctx.respond(em)
    
def load(bot) -> None:
    bot.add_plugin(stats_plugin)

def unload(bot) -> None:
    bot.remove_plugin(stats_plugin)
