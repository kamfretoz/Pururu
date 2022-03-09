import hikari
import lightbulb
from lightbulb.ext import filament
from datetime import datetime, timedelta, timezone

purge_plugin = lightbulb.Plugin("purge", "Burn down the evidence! *evil laugh*")

@purge_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)
@lightbulb.option("amount", "The number of messages to purge.", type=int, required=True, max_value = 500)
@lightbulb.command("purge", "Purge messages from this channel.", aliases=["clear","prune"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def purge_messages(ctx: lightbulb.Context, amount) -> None:
    channel = ctx.channel_id

    # If the command was invoked using the PrefixCommand, it will create a message
    # before we purge the messages, so you want to delete this message first
    if isinstance(ctx, lightbulb.PrefixContext):
        await ctx.event.message.delete()

    messages = await ctx.bot.rest.fetch_messages(channel).limit(amount).take_while(lambda msg: (datetime.now(timezone.utc) - msg.created_at) < timedelta(days=28))
    await ctx.bot.rest.delete_messages(channel, messages)

    await ctx.respond(f"**{len(messages)} messages deleted**", delete_after=5)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge_plugin)