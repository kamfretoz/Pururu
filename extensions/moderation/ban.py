import lightbulb
import hikari
from lightbulb.utils import pag, nav
from hikari.permissions import Permissions

ban_plugin = lightbulb.Plugin("ban", "Prepare the ban hammer!! (Please use it wisely")
ban_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
    lightbulb.guild_only
    )

BAN_PERMISSIONS = (
    Permissions.BAN_MEMBERS
)

@ban_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("reason", "the reason for banning the member", str, required=False, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("duration", "the duration for the ban to be applied", int , required=True)
@lightbulb.option("user", "the user you want to ban", hikari.User , required=True)
@lightbulb.app_command_permissions(BAN_PERMISSIONS, dm_enabled=False)
@lightbulb.command("ban", "ban a member", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ban(ctx: lightbulb.Context, user: hikari.User, delete_message: int, reason: str):
    res = reason or f"'No Reason Provided.' By {ctx.author.username}"
    delete = delete_message or 0

    if delete > 604800:
        delete = 604800

    await ctx.respond(f"Banning **{user.username}**")
    await ctx.bot.rest.ban_member(user = user, guild = ctx.get_guild(), delete_message_seconds=delete, reason = res)
    await ctx.edit_last_response(f"Succesfully banned `{user}` for `{res}`!")
    
@ban_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("reason", "the reason for unbanning the member", str, required=False, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "the user you want to unban (Please use their user ID)", hikari.Snowflake, required=True)
@lightbulb.app_command_permissions(BAN_PERMISSIONS, dm_enabled=False)
@lightbulb.command("unban", "unban a member", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def unban(ctx: lightbulb.Context, user: hikari.Snowflake, reason: str):
    res = reason or f"'No Reason Provided.' By {ctx.author.username}"
    await ctx.respond(f"Unbanning the user ID of **{user}**")
    await ctx.bot.rest.unban_member(user = user, guild = ctx.get_guild(), reason = res)
    await ctx.edit_last_response(f"Succesfully unbanned the ID of `{user}` for `{res}`!")
    
@ban_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.app_command_permissions(BAN_PERMISSIONS, dm_enabled=False)
@lightbulb.command("banlist", "see the list of banned members in this server", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def banlist(ctx: lightbulb.Context):
    bans = await ctx.bot.rest.fetch_bans(ctx.get_guild())
    lst = pag.EmbedPaginator()
    
    @lst.embed_factory()
    def build_embed(page_index,page_content):
        emb = hikari.Embed(title=f"List of Banned Members ({len(bans)})", description=page_content)
        emb.set_footer(f"Page {page_index}")
        return emb
    
    for n, users in enumerate(bans, start=1):
        lst.add_line(f"**{n}. {users.user}** ({users.reason or f'No Reason Provided. (by: {ctx.author.username}'})")
    navigator = nav.ButtonNavigator(lst.build_pages())
    await navigator.run(ctx)
    

def load(bot):
    bot.add_plugin(ban_plugin)

def unload(bot):
    bot.remove_plugin(ban_plugin)
