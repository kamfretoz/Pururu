from datetime import datetime
import hikari
import lightbulb
from lightbulb.utils import pag, nav

server_plugin = lightbulb.Plugin("server", "Server info commands")

@server_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("serverinfo", "Show's the information of the current server", aliases=["si","servinfo"], auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def serverinfo(ctx: lightbulb.Context):
    guild = await ctx.bot.rest.fetch_guild(ctx.guild_id)
    roles = await guild.fetch_roles()
    all_roles = [r.mention for r in roles]
    id = str(guild.id)
    created = int(guild.created_at.timestamp())
    owner = await guild.fetch_owner()
    members = len(guild.get_members().keys())
    verif = guild.verification_level.name.upper()
    role_count = len(guild.get_roles().keys())
    channels = len(guild.get_channels().keys())
    level = guild.premium_tier.value
    boost = guild.premium_subscription_count
    
    emb = hikari.Embed(title=f"Server info for {guild.name}", 
                    colour=ctx.author.accent_color,
                    timestamp=datetime.now().astimezone()
                    )
    
    emb.set_thumbnail(guild.icon_url)
    emb.set_image(guild.banner_url)
    emb.add_field(name="ID", value=id, inline=False)
    emb.add_field(name="Owner", value=f"{owner} ({owner.mention})", inline=False)
    emb.add_field(name="Created At", value=f"<t:{created}:F>\n(<t:{created}:R>)", inline=False)
    emb.add_field(name="Member Count", value=f"{members} Members", inline=True)
    emb.add_field(name="Channel Count", value=f"{channels} Channels", inline=True)
    emb.add_field(name="Verification Level", value=verif, inline=False)
    emb.add_field(name="Server Level", value=f"Level {level} ({boost} Boosts)", inline=False)
        
    if "COMMUNITY" in guild.features:
        emb.add_field(name="Rule Channel", value=f"<#{guild.rules_channel_id}>", inline=False)
    if guild.afk_channel_id:
        emb.add_field(name="AFK Channel", value=f"<#{guild.afk_channel_id}> ({guild.afk_timeout})", inline=False)
    
    if guild.features:
        features = guild.features
        emb.add_field(name="Guild Features", value=", ".join(features).replace("_", " ").title(), inline=False)

    emb.add_field(name=f"Roles ({role_count})", value=", ".join(all_roles) if len(all_roles) < 10 else f"{len(all_roles)} roles", inline=False)
    await ctx.respond(embed=emb)

@server_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("servericon", "Shows the list of member on a particular role", aliases=["si_icon"], auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def server_icon(ctx: lightbulb.Context):
    guild = ctx.bot.cache.get_guild(ctx.guild_id)
    embed = hikari.Embed(title=f"Server Icon for {guild.name}")
    embed.set_image(guild.icon_url)
    await ctx.respond(embed=embed)

@server_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("role", "The role you want to view", hikari.Role)
@lightbulb.command("inrole", "Shows the list of member on a particular role", aliases=["roles","inr"], auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def inrole(ctx: lightbulb.Context, role: hikari.Role) -> None:
    lst = pag.EmbedPaginator()
    count = 0
    @lst.embed_factory()
    def build_embed(page_index,page_content):
        emb = hikari.Embed(title=f"List of members on the '{role.name}' Role.", description=page_content, color=role.color)
        return emb
    
    for member_id in ctx.bot.cache.get_guild(ctx.guild_id).get_members():
        member = ctx.bot.cache.get_guild(ctx.guild_id).get_member(member_id)
        if role.id in member.role_ids:
            lst.add_line(member)
            count += 1
    
    if count == 0:
        await ctx.respond(embed=hikari.Embed(description="No Members found."))
        return
    
    navigator = nav.ButtonNavigator(lst.build_pages())
    await navigator.run(ctx)

def load(bot) -> None:
    bot.add_plugin(server_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(server_plugin)
