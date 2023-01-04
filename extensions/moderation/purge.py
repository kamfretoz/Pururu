import hikari
import lightbulb
from datetime import datetime, timedelta, timezone
from hikari.permissions import Permissions

purge_plugin = lightbulb.Plugin("purge", "Burn down the evidence! *evil laugh*")
purge_plugin.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.guild_only
)
PURGE_PERMISSIONS = (
    Permissions.MANAGE_MESSAGES
)

@purge_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("amount", "The number of messages to purge.", type=int, required=True, max_value = 500)
@lightbulb.app_command_permissions(PURGE_PERMISSIONS, dm_enabled=False)
@lightbulb.command("purge", "Purge messages from this channel.", aliases=["clear","prune"], auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def purge(ctx: lightbulb.Context, amount: int) -> None:
    if amount > 500:
        await ctx.respond(":x: **You can only purge 500 messages at once, max**")
        return

    channel = ctx.channel_id

    iterator = (
                ctx.bot.rest.fetch_messages(channel)
                .limit(amount)
                .take_while(lambda msg: (datetime.now(timezone.utc) - msg.created_at) < timedelta(days=14))
            )
    if iterator:
        async for messages in iterator.chunk(100):
            await ctx.bot.rest.delete_messages(channel, messages)
        await ctx.respond(f"**Messages has been sucessfully deleted.**", delete_after=5)
    else:
        await ctx.respond("Could not find any messages younger than 14 days!")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge_plugin)