import lightbulb
import hikari
import datetime

timeout_plugin = lightbulb.Plugin("timeout")
timeout_plugin.add_checks(lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))

@timeout_plugin.command()
@lightbulb.option("hour", "the duration of the timeout (hour)", hikari.OptionType.INTEGER, required=False)
@lightbulb.option("minute", "the duration of the timeout (minute)", hikari.OptionType.INTEGER, required=False)
@lightbulb.option("second", "the duration of the timeout (second)", hikari.OptionType.INTEGER, required=False)
@lightbulb.option("user", "the user you want to be put in timeout", hikari.OptionType.USER, required=True)
@lightbulb.command("timeout", "Timeout a member")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def timeout(ctx: lightbulb.Context):
    user = ctx.options.user
    hour = ctx.options.hour or 0
    min = ctx.options.minute or 0
    sec = ctx.options.second or 0
    timeout = datetime.datetime.now().astimezone() + datetime.timedelta(hours=hour, minutes=min, seconds=sec)
    if hour is 0 and min is 0 and sec is 0:
        await ctx.respond(f"Removing timeout from {user}")
    else:
        await ctx.respond(f"Attempting to timeout {user}")
    await ctx.bot.rest.edit_member(user = user, guild = ctx.get_guild(), communication_disabled_until=timeout)
    await ctx.edit_last_response("Task finished successfully!")
    
def load(bot):
    bot.add_plugin(timeout_plugin)

def unload(bot):
    bot.remove_plugin(timeout_plugin)
