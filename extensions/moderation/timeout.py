import lightbulb
import hikari
from datetime import datetime, timedelta, timezone

timeout_plugin = lightbulb.Plugin("timeout")
timeout_plugin.add_checks(lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))

@timeout_plugin.command()
@lightbulb.option("reason", "the reason for the timeout", hikari.OptionType.STRING, required=False)
@lightbulb.option("days", "the duration of the timeout (days)", hikari.OptionType.INTEGER, required=False, default=0)
@lightbulb.option("hour", "the duration of the timeout (hour)", hikari.OptionType.INTEGER, required=False, default=0)
@lightbulb.option("minute", "the duration of the timeout (minute)", hikari.OptionType.INTEGER, required=False, default=0)
@lightbulb.option("second", "the duration of the timeout (second)", hikari.OptionType.INTEGER, required=False, default=0)
@lightbulb.option("user", "the user you want to be put in timeout", hikari.OptionType.USER, required=True)
@lightbulb.command("timeout", "Timeout a member")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def timeout(ctx: lightbulb.Context):
    user = ctx.options.user
    reason = ctx.options.timeout
    days = ctx.options.days
    hour = ctx.options.hour
    min = ctx.options.minute
    sec = ctx.options.second
    
    now = datetime.now(timezone.utc)
    then = now + timedelta(days=days, hours=hour, minutes=min, seconds=sec)
    
    if (then - now).days > 28:
        await ctx.respond("You can't time someone out for more than 28 days")
        return
    
    if days is 0 and hour is 0 and min is 0 and sec is 0:
        await ctx.respond(f"Removing timeout from **{user}**")
    else:
        await ctx.respond(f"Attempting to timeout **{user}**")
    await ctx.bot.rest.edit_member(user = user, guild = ctx.get_guild(), communication_disabled_until=then, reason=reason)
    await ctx.edit_last_response("Task finished successfully!")
    
def load(bot):
    bot.add_plugin(timeout_plugin)

def unload(bot):
    bot.remove_plugin(timeout_plugin)
