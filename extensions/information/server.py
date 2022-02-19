from datetime import datetime
import hikari
import lightbulb

server_plugin = lightbulb.Plugin("server", "Server info commands")

@server_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("serverinfo", "Show's the information of the current server", aliases=["si"], auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def serverinfo(ctx: lightbulb.Context):
    guild = ctx.bot.cache.get_guild(ctx.guild_id)
    roles = await guild.fetch_roles()
    all_roles = [r.mention for r in roles]
    id = guild.id
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
    emb.add_field(name="Created At", value=f"<t:{created}:d>\n(<t:{created}:R>)", inline=False)
    emb.add_field(name="Member Count", value=f"{members} Members", inline=False)
    emb.add_field(name="Channel Count", value=f"{channels} Channels", inline=False)
    emb.add_field(name="Verification Level", value=verif, inline=False)
    emb.add_field(name="Server Level", value=f"Level {level} ({boost} Boosts.)", inline=False)
        
    if "COMMUNITY" in guild.features:
        emb.add_field(name="Rule Channel", value=f"<#{guild.rules_channel_id}>", inline=False)
    if guild.afk_channel_id:
        emb.add_field(name="AFK Channel", value=f"<#{guild.afk_channel_id}> ({guild.afk_timeout})", inline=False)
    
    if guild.features:
        features = guild.features
        emb.add_field(name="Guild Features", value=", ".join(features).replace("_", " ").title(), inline=False)

    emb.add_field(name=f"Roles ({role_count})", value=", ".join(all_roles) if len(all_roles) < 10 else f"{len(all_roles)} roles", inline=False)
    await ctx.respond(embed=emb)


def load(bot) -> None:
    bot.add_plugin(server_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(server_plugin)
