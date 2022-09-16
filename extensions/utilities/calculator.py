import lightbulb
import hikari
from operator import pow, truediv, mul, add, sub, floordiv
from lightbulb.ext import filament

calc_plugin = lightbulb.Plugin("calculator", "It's a simple calculator, what did you expect?")

operators = {
    '+' : add,
    '-' : sub,
    '*' : mul,
    '/' : truediv,
    '//': floordiv,
    '^' : pow
}

def calculate(s):
    if s.isdigit():
        return float(s)
    for c in operators.keys():
        left, operator, right = s.partition(c)
        if operator in operators:
            return operators[operator](calculate(left), calculate(right))

@calc_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.set_help(text="Simple calculator, From ℤ to ℤ only.")
@lightbulb.option("calculation", "The operation you want to perform", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("calculator", "Calculate the given value", aliases=["calc"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def calc(ctx: lightbulb.Context, calculation: str) -> None:
    em = hikari.Embed(color=0xD3D3D3, title="Calculator")
    try:
        em.add_field(name="Input:", value=calculation, inline=False,)
        em.add_field(name="Output:", value=str(calculate(calculation.replace(
            "**", "^").replace("x", "*").replace(" ", "").strip())), inline=False)
    except Exception as e:
        raise ValueError(f"An Error Occured! {e}")
    await ctx.respond(embed=em)

def load(bot):
    bot.add_plugin(calc_plugin)

def unload(bot):
    bot.remove_plugin(calc_plugin)
