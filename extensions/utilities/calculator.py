import lightbulb
import hikari
from operator import pow, truediv, mul, add, sub

calc_plugin = lightbulb.Plugin("calculator", "It's a calculator, what did you expect?")

@calc_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("right", "The rightmost value", int, required=True)
@lightbulb.option("operation", "The operation you want to perform", str, required=True, choices=["+","-","*","/","^"])
@lightbulb.option("left", "The leftmost value", int, required=True)
@lightbulb.command("calculator", "Calculate the given value", aliases=["calc"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def calc(ctx: lightbulb.Context) -> None:
    calculation = f"{ctx.options.left}{ctx.options.operation}{ctx.options.right}"
    
    calculation.strip()
    
    operators = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
        '^': pow
    }
    def calculate(s):
        if s.isdigit():
            return float(s)
        for c in operators.keys():
            left, operator, right = s.partition(c)
            if operator in operators:
                return operators[operator](calculate(left), calculate(right))
    em = hikari.Embed(color=0xD3D3D3, title="Calculator")
    try:
        em.add_field(name="Input:", value=calculation, inline=False,)
        em.add_field(name="Output:", value=str(calculate(calculation.replace(
            "**", "^").replace("x", "*").replace(" ", "").strip())), inline=False)
    except Exception as e:
        raise ValueError(f"An Error Occured! {e}")
    await ctx.respond(content=None, embed=em)

def load(bot):
    bot.add_plugin(calc_plugin)

def unload(bot):
    bot.remove_plugin(calc_plugin)
