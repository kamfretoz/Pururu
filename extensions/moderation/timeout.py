import lightbulb
import hikari
from datetime import datetime, timedelta, timezone

timeout_plugin = lightbulb.Plugin("timeout", "timeout for a moment.")
timeout_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)

@timeout_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("reason", "the reason for the timeout", str, required=False,modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("days", "the duration of the timeout (days)", int, required=False, default=0)
@lightbulb.option("hour", "the duration of the timeout (hour)", int, required=False, default=0)
@lightbulb.option("minute", "the duration of the timeout (minute)", int, required=False, default=0)
@lightbulb.option("second", "the duration of the timeout (second)", int, required=False, default=0)
@lightbulb.option("user", "the user you want to be put in timeout", hikari.Member , required=True)
@lightbulb.command("timeout", "Timeout a member", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def timeout(ctx: lightbulb.Context, user: hikari.Member, second: int, minute: int, hour: int , days: int, reason: str):
    
    res = reason or f"No Reason Provided. By: {ctx.author}"
    
    now = datetime.now(timezone.utc)
    then = now + timedelta(days=days, hours=hour, minutes=minute, seconds=second)
    
    if (then - now).days > 28:
        await ctx.respond("You can't time someone out for more than 28 days")
        return
    
    if days == 0 and hour == 0 and minute == 0 and second == 0:
        await ctx.respond(f"Removing timeout from **{user}**")
        txt = f"Timeout for {user.mention} has been removed successfully!"
    else:
        await ctx.respond(f"Attempting to timeout **{user}**")
        txt = f"The user {user.mention} has been timed out until <t:{int(then.timestamp())}:R>"
    await ctx.bot.rest.edit_member(user = user, guild = ctx.get_guild(), communication_disabled_until=then, reason=res)
    await ctx.edit_last_response(txt)
    
def load(bot):
    bot.add_plugin(timeout_plugin)

def unload(bot):
    bot.remove_plugin(timeout_plugin)
