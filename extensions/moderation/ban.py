import lightbulb
import hikari
from lightbulb.utils import pag, nav

ban_plugin = lightbulb.Plugin("ban")
ban_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.BAN_MEMBERS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.BAN_MEMBERS)
    )

@ban_plugin.command()
@lightbulb.option("reason", "the reason for banning the member", hikari.OptionType.STRING, required=False, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("delete_message", "Delete the messages after the ban? (up to 7 days, leave empty or set to 0 to not delete)", hikari.OptionType.INTEGER, min_value = 0, max_value = 7, default = 0 ,required=False)
@lightbulb.option("user", "the user you want to ban", hikari.OptionType.USER, required=True)
@lightbulb.command("ban", "ban a member")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def ban(ctx: lightbulb.Context):
    user = ctx.options.user
    res = ctx.options.reason or f"'No Reason Provided.' By {ctx.author.username}"
    delete = ctx.options.delete_message or 0
    await ctx.respond(f"Banning **{user}**")
    await ctx.bot.rest.ban_member(user = user, guild = ctx.get_guild(), reason = res, delete_message_days=delete)
    await ctx.edit_last_response(f"Succesfully banned `{user}` for `{res}`!")
    
@ban_plugin.command()
@lightbulb.option("reason", "the reason for unbanning the member", hikari.OptionType.STRING, required=False, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "the user you want to unban", hikari.OptionType.MENTIONABLE, required=True)
@lightbulb.command("unban", "unban a member")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def unban(ctx: lightbulb.Context):
    user = ctx.options.user
    res = ctx.options.reason or f"'No Reason Provided.' By {ctx.author.username}"
    await ctx.respond(f"Unbanning **{user}**")
    await ctx.bot.rest.unban_member(user = user, guild = ctx.get_guild(), reason = res)
    await ctx.edit_last_response(f"Succesfully unbanned `{user}` for `{res}`!")
    
@ban_plugin.command()
@lightbulb.command("bans", "see the list of banned members in this server")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def banlist(ctx: lightbulb.Context):
    bans = await ctx.bot.rest.fetch_bans(ctx.get_guild())
    lst = pag.EmbedPaginator()
    
    @lst.embed_factory()
    def build_embed(page_index,page_content):
        emb = hikari.Embed(title="List of Banned Members", description=page_content)
        emb.set_footer(f"{len(bans)} Members in total.")
        return emb
    
    for users in bans:
            lst.add_line(str(users.user))
    
    navigator = nav.ButtonNavigator(lst.build_pages())
    await navigator.run(ctx)
    
    

def load(bot):
    bot.add_plugin(ban_plugin)

def unload(bot):
    bot.remove_plugin(ban_plugin)
