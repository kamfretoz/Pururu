import lightbulb
import random
from lightbulb.ext import filament

text_plugin = lightbulb.Plugin("texts", "Many kind of text manipulation tools!")

@text_plugin.command
@lightbulb.option("text", "The text you want to drunkify", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("mock", "iTS SpElleD sQl!!", aliases=["drunkify"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
@filament.utils.pass_options
async def mock(ctx: lightbulb.Context, text: str):
    """
    iTS SpElleD sQl!!
    """
    lst = [str.upper, str.lower]
    newText = ''.join(random.choice(lst)(c) for c in text)
    if len(newText) <= 1024:
        await ctx.respond(newText)
    else:
        try:
            await ctx.author.send(newText)
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")

@text_plugin.command
@lightbulb.option("text", "The text you want to reverse", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("gap", "The gap between each T E X T", int, min_value = 1, max_value = 5)
@lightbulb.command("expand", "E X P A N D the T E X T", aliases=["enlarge"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
@filament.utils.pass_options
async def expand(ctx:lightbulb.Context, gap: int, text: str):
    spacing = ""
    if gap > 0 and gap <= 5:
        for _ in range(gap):
            spacing += " "
        result = spacing.join(text)
        if len(result) <= 1000:
            await ctx.respond(result)
        else:
            await ctx.respond(f"**{ctx.author.mentiona}, The output too was too large!")
    else:
        await ctx.respond("```Error: The number can only be from 1 to 5```")

@text_plugin.command
@lightbulb.option("text", "The text you want to reverse", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("reverse", "txeT eht esreveR", aliases=["rev"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
@filament.utils.pass_options
async def reverse(ctx: lightbulb.Context, text: str):
    result = text[::-1]
    if len(result) <= 2000:
        await ctx.respond(f"{result}")
    else:
        await ctx.respond(f"**{ctx.author.mention}, The output too was too large!**")
            
@text_plugin.command
@lightbulb.option("text", "the text to be put in codeblock", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("codeblock", "wrap a text inside a codeblock", aliases=["cb"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
@filament.utils.pass_options
async def codeblock(ctx: lightbulb.Context, text: str):
    """Write text in code format."""
    if len(text) <= 1900:
        await ctx.respond("```" + text.replace("`", "") + "```")
    else:
        await ctx.respond(f"**{ctx.author.mention}, The output too was too large!**")

def load(bot):
    bot.add_plugin(text_plugin)

def unload(bot):
    bot.remove_plugin(text_plugin)