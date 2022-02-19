from datetime import datetime
from lightbulb.ext import filament
import hikari
import lightbulb

user_plugin = lightbulb.Plugin("user", "User lookup commands")

@user_plugin.command
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("memberinfo", "Get info on a server member.", aliases=["mi","profile","minfo"], ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand, lightbulb.UserCommand)
@filament.utils.pass_options
async def  member_info(ctx: lightbulb.Context, target) -> None:
    target = ctx.get_guild().get_member(target or ctx.user)

    if not target:
        await ctx.respond("That user is not in the server, use the userinfo command instead.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone
    emb = hikari.Embed(
        title=f"User Info - {target.display_name}",
        description=f"ID: `{target.id}`",
        colour=target.accent_color,
        timestamp=datetime.now().astimezone(),
    )
    emb.set_footer(
        text=f"Requested by {ctx.member.display_name}",
        icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
    )
    emb.set_thumbnail(target.avatar_url or target.default_avatar_url)
    emb.add_field(
        "Bot?",
        str(target.is_bot),
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
        ", ".join(r.mention for r in roles),
        inline=False,
    )
    emb.add_field(
        "Mention", 
        target.mention, 
        inline=False
    )
    
    await ctx.respond(emb)
    
@user_plugin.command
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("userinfo", "Get info on a server member.", aliases=["ui","uprofile","uinfo"], ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def  user_info(ctx: lightbulb.Context, target) -> None:
    target = await ctx.bot.rest.fetch_user(user = target or ctx.user)
    
    if not target:
        await ctx.respond("Cannot find that user.")
        return
    created_at = int(target.created_at.timestamp())
    emb = hikari.Embed(
            title=f"User Info - {target}",
            description=f"ID: `{target.id}`",
            colour=target.accent_color,
            timestamp=datetime.now().astimezone(),
        )
    emb.add_field(name="Is bot?", value=target.is_bot, inline=False)
    emb.set_thumbnail(target.avatar_url or target.default_avatar_url)
    if target.banner_url:
        emb.set_image(target.banner_url)
    emb.add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=False,
    )
    emb.add_field(name="Mention", value=target.mention, inline=False)
    
    await ctx.respond(embed=emb)

@user_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("target", "The member to get the banner.", hikari.Member, required=True)
@lightbulb.command("banner", "Get a member's banner.", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand, lightbulb.UserCommand)
@filament.utils.pass_options
async def user_banner(ctx: lightbulb.Context, target):
    """Show the banner of a user, if any"""
    target = await ctx.bot.rest.fetch_user(user = target or ctx.user)

    if not target:
        await ctx.respond("That user is not in the server.")
        return
    
    banner = target.banner_url
    # If statement because the user may not have a banner
    if banner:
        bnr = hikari.Embed(
                description=f"**{target.mention}**'s Banner",
                title="Banner Viewer",
                color=target.accent_colour,
                timestamp=datetime.now().astimezone(),
            )
        bnr.set_image(banner)
        await ctx.respond(embed=bnr)
    else:
        await ctx.respond(embed=hikari.Embed(description="This User has no banner set."))
        
@user_plugin.command
@lightbulb.option("server", "Get the server avatar instead?", bool, required = False, default = True)
@lightbulb.option("target", "The member to get the avatar.", hikari.User , required=True)
@lightbulb.command("avatar", "Get a member's avatar.", auto_defer=True, aliases=["pp", "pfp","ava","icon"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand, lightbulb.UserCommand)
@filament.utils.pass_options
async def user_avatar(ctx: lightbulb.Context, target: hikari.User, server: bool):
    """Show avatar of a user, if any"""
    target = target or ctx.user

    if not target:
        await ctx.respond("That user is not in the server.")
        return
    
    if server:
        pfp = target.guild_avatar_url or target.avatar_url
    else:
        pfp = target.avatar_url or target.default_avatar_url
    # If statement because the user may not have a custom avatar
    if pfp:
        ava = hikari.Embed(
                description=f"**{target.mention}**'s Avatar",
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
