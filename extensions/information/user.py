from datetime import datetime

import hikari
import lightbulb

user_plugin = lightbulb.Plugin("user")

@user_plugin.command
@lightbulb.command("info", "All the info lookup commands you'll ever need")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def user_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

@user_group.child
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("user", "Get info on a server member.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def user_info(ctx: lightbulb.Context) -> None:
    target = ctx.options.target or ctx.user

    if not target:
        await ctx.respond("That user is not in the server.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone

    embed = (
        hikari.Embed(
            title=f"User Info - {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=0x3B9DFF,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_thumbnail(target.avatar_url or target.default_avatar_url)
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=False,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=False,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=False,
        )
        .add_field(
            "Roles",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
    )

    await ctx.respond(embed)

@user_group.child
@lightbulb.option("target", "The member to get the banner.", hikari.User, required=True)
@lightbulb.command("banner", "Get a member's banner.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def user_banner(ctx: lightbulb.Context):
    """Show the banner of a user, if any"""
    target = await ctx.bot.rest.fetch_user(user = ctx.options.target or ctx.user)

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
        


def load(bot) -> None:
    bot.add_plugin(user_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(user_plugin)
