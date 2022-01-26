import lightbulb
import hikari


ext_plugin = lightbulb.Plugin("extras", "for commands that are so random that i dont know where to put them")

@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.command("why", "Askin the real question here", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def whytho(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/why') as why:
        data = await why.json()
        result = data.get('why')
        embed = hikari.Embed(
            description=result, color=0x8253c3)
        await ctx.respond(embed=embed)
        
@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.command("name", "A random name generator", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def namedeez(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/name') as name:
            data = await name.json()
            result = data.get('name')
            embed = hikari.Embed(
                description=result, color=0x8253c3)
            await ctx.respond(embed=embed)
    
def load(bot):
    bot.add_plugin(ext_plugin)

def unload(bot):
    bot.remove_plugin(ext_plugin)
