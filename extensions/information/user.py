from datetime import datetime
from lightbulb.ext import filament
import hikari
import lightbulb

user_plugin = lightbulb.Plugin("user", "User lookup commands")

@user_plugin.command
@lightbulb.option("target", "The member to get information about.", hikari.Member, required=False)
@lightbulb.command("memberinfo", "Get info on a server member.", aliases=["mi","profile","minfo", "ui", "userinfo"], ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def  member_info(ctx: lightbulb.Context, target: hikari.Member) -> None:
    if target is None:
        target = ctx.member
    
    user = ctx.get_guild().get_member(target)

    if not user:
        await ctx.respond("That user is not in the server, use the userinfo command instead.")
        return

    created_at = int(user.created_at.timestamp())
    joined_at = int(user.joined_at.timestamp())

    roles = (await user.fetch_roles())[1:]  # All but @everyone
    
    
    
    emb = hikari.Embed(
        title=f"User Info - {user.display_name}",
        description=f"ID: `{user.id}`",
        colour=user.accent_color,
        timestamp=datetime.now().astimezone(),
    )
    emb.set_footer(
        text=f"Requested by {ctx.member.display_name}",
        icon=ctx.member.avatar_url or ctx.member.default_avatar_url
    )
    emb.set_thumbnail(user.avatar_url or user.default_avatar_url)
    emb.add_field(
        "Bot?",
        str(user.is_bot),
        inline=False,
    )
    emb.add_field(
        "Created account on",
        f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
        inline=False,
    )
    emb.add_field(
        "Joined server on",
        f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
        inline=False,
    )
    emb.add_field(
        "Roles",
        ", ".join(r.mention for r in roles) or "No Roles.",
        inline=False,
    )
    emb.add_field(
        "Mention", 
        user.mention, 
        inline=False
    )
    
    await ctx.respond(emb)

@user_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("target", "The member to get the banner.", hikari.User, required=False)
@lightbulb.command("banner", "Get a member's banner.", auto_defer = True, ephemeral = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def user_banner(ctx: lightbulb.Context, target: hikari.User):
    """Show the banner of a user, if any"""
    if target is None:
        target = ctx.user
    
    user = await ctx.bot.rest.fetch_user(target)

    if not user:
        await ctx.respond("That user is not in the server.")
        return
    
    banner = user.banner_url
    # If statement because the user may not have a banner
    if banner:
        bnr = hikari.Embed(
                description=f"**{user.mention}**'s Banner",
                title="Banner Viewer",
                color=user.accent_colour,
                timestamp=datetime.now().astimezone(),
            )
        bnr.set_image(banner)
        await ctx.respond(embed=bnr)
    else:
        await ctx.respond(embed=hikari.Embed(description="This User has no banner set."))
        
@user_plugin.command
@lightbulb.option("server", "Get the server avatar instead?", bool, required = False, default = False)
@lightbulb.option("target", "The member to get the avatar.", hikari.Member , required=False)
@lightbulb.command("avatar", "Get a member's avatar.", auto_defer=True, aliases=["pp", "pfp","ava","icon"], ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def user_avatar(ctx: lightbulb.Context, target: hikari.Member, server: bool):
    """Show avatar of a user, if any"""
    if target is None:
        target = ctx.member
        
    user =  ctx.get_guild().get_member(target)

    if not user:
        await ctx.respond("That user is not in the server.")
        return
    
    if server:
        try:
            pfp = user.guild_avatar_url
        except AttributeError:
            return await ctx.respond("That user doesn't have server-specific avatar.")
    else:
        pfp = target.avatar_url or target.default_avatar_url
    # If statement because the user may not have a custom avatar
    if pfp:
        ava = hikari.Embed(
                description=f"**{user.mention}**'s Avatar",
                title="Avatar Viewer",
                color=target.accent_colour,
                timestamp=datetime.now().astimezone(),
            )
        ava.set_image(pfp)
        await ctx.respond(embed=ava)
    else:
        await ctx.respond(embed=hikari.Embed(description="This User has no avatar set."))

def load(bot) -> None:
    bot.add_plugin(user_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(user_plugin)
