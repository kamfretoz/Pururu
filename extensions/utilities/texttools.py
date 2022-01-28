from pydoc import text
import lightbulb
import hikari
import random

text_plugin = lightbulb.Plugin("texttools", "Many kind of text manipulation tools!")

@text_plugin.command()
@lightbulb.command("text", "text manipulation tools at your disposal!")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def texttools(ctx: lightbulb.Context) -> None:
    pass

@texttools.child
@lightbulb.option("text", "The text you want to drunkify", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("mock", "iTS SpElleD sQl!!", aliases=["drunkify"])
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def mock(ctx: lightbulb.Context):
    """
    iTS SpElleD sQl!!
    """
    txt = ctx.options.text
    lst = [str.upper, str.lower]
    newText = ''.join(random.choice(lst)(c) for c in txt)
    if len(newText) <= 1024:
        await ctx.respond(newText)
    else:
        try:
            await ctx.author.send(newText)
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

@texttools.child
@lightbulb.option("text", "The text you want to reverse", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("gap", "The gap between each T E X T", int, min_value = 1, max_value = 5)
@lightbulb.command("expand", "E X P A N D the T E X T", aliases=["enlarge"])
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def expand(ctx:lightbulb.Context):
    gap = ctx.options.gap
    txt = ctx.options.text

    spacing = ""
    if gap > 0 and gap <= 5:
        for _ in range(gap):
            spacing += " "
        result = spacing.join(txt)
        if len(result) <= 256:
            await ctx.respond(result)
        else:
            try:
                await ctx.author.send(result)
                await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
            except Exception:
                await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
    else:
        await ctx.respond("```Error: The number can only be from 1 to 5```")

@texttools.child
@lightbulb.option("text", "The text you want to reverse", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("reverse", "txeT eht esreveR", aliases=["rev"])
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def reverse(ctx: lightbulb.Context):
    txt = ctx.options.text
    result = txt[::-1]
    if len(result) <= 512:
        await ctx.respond(f"{result}")
    else:
        try:
            await ctx.author.send(f"{result}")
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
            
@texttools.child
@lightbulb.option("text", "the text to be put in codeblock", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("codeblock", "wrap a text inside a codeblock", aliases=["cb"])
async def codeblock(ctx: lightbulb.Context):
    """Write text in code format."""
    msg = ctx.options.text
    await ctx.respond("```" + msg.replace("`", "") + "```")

def load(bot):
    bot.add_plugin(text_plugin)

def unload(bot):
    bot.remove_plugin(text_plugin)