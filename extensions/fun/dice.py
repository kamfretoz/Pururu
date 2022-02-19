import random

import lightbulb
from lightbulb.ext import filament

dice_plugin = lightbulb.Plugin("dice", "Roll the dice!")

@dice_plugin.command
# These two are the same type, but are optional. We can provide a
# default value simply by using the `default` kwarg.
@lightbulb.option("bonus", "A fixed number to add to the total roll.", int, default=0)
@lightbulb.option("sides", "The number of sides each die will have.", int, default=6)
# The options the command will have. This creates a required int
# option. Validation is handled for you -- Discord won't let you
# send the command unless it's a number. How cool is that?!
@lightbulb.option("number", "The number of dice to roll.", int)
# Convert the function into a command
@lightbulb.command("dice", "Roll one or more dice.")
# Define the types of command that this function will implement
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
@filament.utils.pass_options
async def dice(ctx: lightbulb.Context, number: int, sides: int, bonus: int) -> None:
    # Option validation
    if number > 25:
        await ctx.respond("No more than 25 dice can be rolled at once.")
        return

    if sides > 100:
        await ctx.respond("The dice cannot have more than 100 sides.")
        return

    rolls = [random.randint(1, sides) for _ in range(number)]

    # To send a message, use ctx.respond. Using kwargs, you can make the
    # bot reply to a message (when not sent from a slash command
    # invocation), allow mentions, make the message ephemeral, etc.
    await ctx.respond(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(dice_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(dice_plugin)
