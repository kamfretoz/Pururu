import asyncio

import hikari
import lightbulb

purge_plugin = lightbulb.Plugin("purge")

@purge_plugin.command
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)
@lightbulb.option("amount", "The number of messages to purge.", type=int, required=True)
@lightbulb.command("purge", "Purge messages from this channel.", aliases=["clear"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def purge_messages(ctx: lightbulb.Context) -> None:
    num_msgs = ctx.options.amount
    channel = ctx.channel_id

    # If the command was invoked using the PrefixCommand, it will create a message
    # before we purge the messages, so you want to delete this message first
    if isinstance(ctx, lightbulb.PrefixContext):
        await ctx.event.message.delete()

    msgs = await ctx.bot.rest.fetch_messages(channel).limit(num_msgs)
    await ctx.bot.rest.delete_messages(channel, msgs)

    resp = await ctx.respond(f"{len(msgs)} messages deleted")

    await asyncio.sleep(5)
    await resp.delete()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge_plugin)