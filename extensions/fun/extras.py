import lightbulb
import hikari
from random import choice


ext_plugin = lightbulb.Plugin("extras", "for commands that are so random that i dont know where to put them", include_datastore=True)

@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("why", "Askin the real question here", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def whytho(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/why') as why:
        data = await why.json()
        result = data.get('why')
        embed = hikari.Embed(
            description=result, color=0x8253c3)
        await ctx.respond(embed=embed)
        
@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("name", "A random name generator", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def namedeez(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/name') as name:
            data = await name.json()
            result = data.get('name')
            embed = hikari.Embed(
                description=result, color=0x8253c3)
            await ctx.respond(embed=embed)
            
@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("rickroll", "You have been rickrolled!", aliases = ["rr"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def rickroll(ctx: lightbulb.Context):
    rick = hikari.Embed()
    rick.set_image("https://i.kym-cdn.com/photos/images/original/000/041/494/1241026091_youve_been_rickrolled.gif")
    await ctx.respond(embed=rick)

ext_plugin.d.ps = {
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

@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("question", "the question you want to ask", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST, pass_options=True)
@lightbulb.command("8ball", "Ask a question to the 8Ball!")
@lightbulb.implements(lightbulb.PrefixCommand)
async def eightball(ctx: lightbulb.Context, question: str):
    choices = choice(choice(list(ext_plugin.d.ps.values())))
    if choices in ext_plugin.d.ps["psbad"]:
        color = hikari.Color(0xFF0000)
    else:
        color = hikari.Color(0x26D934)
    eightball = hikari.Embed(color=color)
    eightball.add_field(name="Question:", value=question.capitalize(), inline=False)
    eightball.add_field(name="Answer:", value=f"{choices}.")
    eightball.set_author(name = "The mighty 8-Ball")
    eightball.set_footer(f"Requested by: {ctx.author.username}", icon=ctx.author.avatar_url)
    eightball.set_thumbnail("https://i.imgur.com/Q9dxpTz.png")
    await ctx.respond(embed=eightball)

@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("text", "what do you want to pay respect to?", required = False,  modifier = lightbulb.commands.OptionModifier.CONSUME_REST, pass_options = True)
@lightbulb.command("f", "Press F to pay respect.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def respect(ctx: lightbulb.Context, text: str):
    hearts = ['❤', '💛', '💚', '💙', '💜', '♥']
    reason = f"for **{text}** " if text else ""
    await ctx.respond(f"**{ctx.author.username}** has paid their respect {reason}{choice(hearts)}")

@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("reason", "the reason for banning the member", str, required=False, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "the user you want to ban", hikari.Member , required=True)
@lightbulb.command("fakeban", "ban a member (Or is it?)", aliases=["fban"], pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def fakeban(ctx: lightbulb.Context, user: hikari.Member, reason: str):
    await ctx.respond(f"Succesfully banned {user.mention} for `{reason}`!")
    
@ext_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("reason", "the reason for muting the member", str, required=False, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "the user you want to mute", hikari.Member , required=True)
@lightbulb.command("fakemute", "mute a member (Or is it?)", aliases=["fmute"], pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def fakemute(ctx: lightbulb.Context, user: hikari.Member, reason: str):
    await ctx.respond(f"Succesfully muted {user.mention} for `{reason}`!")
    

def load(bot):
    bot.add_plugin(ext_plugin)

def unload(bot):
    bot.remove_plugin(ext_plugin)
