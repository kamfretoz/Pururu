import lightbulb
import hikari

slowmode_plugin = lightbulb.Plugin("slowmode")
slowmode_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_CHANNELS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.MANAGE_CHANNELS)
    )

@slowmode_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("interval", "The interval amount (in seconds)", int, min_value = 0, max_value = 21600, required=False)
@lightbulb.option("channel", "The channel you want to set", hikari.GuildChannel, required=True)
@lightbulb.command("slowmode", "Set the slowmode interval for a channel")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def slowmode(ctx: lightbulb.Context):
    ch = ctx.options.channel
    time = ctx.options.interval or 0
    if time == 0:
        await ctx.respond(f"Removing slow mode from the selected channel")
    else:
        await ctx.respond(f"Attempting to set slowmode on the selected channel for **{time} seconds**")
    await ctx.bot.rest.edit_channel(ch, rate_limit_per_user=time)
    await ctx.edit_last_response("Task Finished Successfully!")
    
def load(bot):
    bot.add_plugin(slowmode_plugin)

def unload(bot):
    bot.remove_plugin(slowmode_plugin)
