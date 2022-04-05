import lightbulb
import hikari

slowmode_plugin = lightbulb.Plugin("slowmode", "*talks in slow motion*")
slowmode_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.CHANGE_NICKNAME),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.CHANGE_NICKNAME)
    )

@slowmode_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("nick", "the new nickname you want to set (leave empty to reset!)", str, required=False)
@lightbulb.option("member", "The member you want to change the nickname", hikari.Member, required=True)
@lightbulb.command("nickname", "Change the nickname of a member")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def nickname(ctx: lightbulb.Context, member: hikari.Member, nick: str):
    await ctx.bot.rest.edit_member(ctx.guild_id, user=member, nickname=nick)
    await ctx.respond(f"Changed {member.mention} nickname to {nick}!")
    
def load(bot):
    bot.add_plugin(slowmode_plugin)

def unload(bot):
    bot.remove_plugin(slowmode_plugin)
