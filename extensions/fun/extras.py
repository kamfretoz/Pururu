import lightbulb
import hikari
from random import choice
from lightbulb.ext import filament


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
            
@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.command("rickroll", "You have been rickrolled!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def rickroll(ctx: lightbulb.Context):
    rick = hikari.Embed()
    rick.set_image("https://i.kym-cdn.com/photos/images/original/000/041/494/1241026091_youve_been_rickrolled.gif")
    await ctx.respond(embed=rick)

@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("question", "the question you want to ask", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("8ball", "Ask a question to the 8Ball!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def eball(ctx: lightbulb.Context, question: str):
    ps = {
        "psgood": [
            "Yes",
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes - definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
        ],
        "psbad": [
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
            "No",
        ],
    }
    choices = choice(choice(list(ps.values())))
    if choices in ps["psbad"]:
        color = hikari.Color(0xFF0000)
    elif choices in ps["psgood"]:
        color = hikari.Color(0x26D934)
    eightball = hikari.Embed(color=color)
    eightball.add_field(name="Question:", value=question.capitalize(), inline=False)
    eightball.add_field(name="Answer:", value=f"{choices}.")
    eightball.set_author(name = "The mighty 8-Ball")
    eightball.set_footer(f"Requested by: {ctx.author.username}", icon=ctx.author.avatar_url)
    eightball.set_thumbnail("https://i.imgur.com/Q9dxpTz.png")
    await ctx.respond(embed=eightball)

@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("text", "what do you want to pay respect to?", required = False,  modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("f", "Press F to pay respect.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def respect(ctx: lightbulb.Context, text: str):
    hearts = ['❤', '💛', '💚', '💙', '💜', '♥']
    reason = f"for **{text}** " if text else ""
    await ctx.respond(f"**{ctx.author.username}** has paid their respect {reason}{choice(hearts)}")

def load(bot):
    bot.add_plugin(ext_plugin)

def unload(bot):
    bot.remove_plugin(ext_plugin)
