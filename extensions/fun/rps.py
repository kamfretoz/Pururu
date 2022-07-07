import random
from enum import Enum

import hikari
import lightbulb
import miru

rps_plugin = lightbulb.Plugin("rps", "Rock Paper Scissor!")


class Sign(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3


class PromptView(miru.View):
    async def view_check(self, ctx: miru.Context) -> bool:
        return ctx.user.id == ctx.message.interaction.user.id


class RockButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Rock", emoji="✊")

    async def callback(self, ctx: miru.Context) -> None:
        # You can access the view an item is attached to by accessing its view property
        self.view.result = Sign.ROCK.name
        self.disabled = True
        self.view.stop()


class PaperButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Paper", emoji="🖐")

    async def callback(self, ctx: miru.Context) -> None:
        # You can access the view an item is attached to by accessing its view property
        self.view.result = Sign.PAPER.name
        self.disabled = True
        self.view.stop()


class ScissorButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Scissor", emoji="✌")

    async def callback(self, ctx: miru.Context) -> None:
        # You can access the view an item is attached to by accessing its view property
        self.view.result = Sign.SCISSOR.name
        self.disabled = True
        self.view.stop()


def play(user_action, computer_action) -> str:
    if user_action == computer_action:
        return f"Both players selected {user_action}. It's a tie!"
    elif user_action == "ROCK":
        if computer_action == "SCISSOR":
            return "Rock smashes scissors! You win!"
        else:
            return "Paper covers rock! You lose."
    elif user_action == "PAPER":
        if computer_action == "ROCK":
            return "Paper covers rock! You win!"
        else:
            return "Scissors cuts paper! You lose."
    elif user_action == "SCISSOR":
        if computer_action == "PAPER":
            return "Scissors cuts paper! You win!"
        else:
            return "Rock smashes scissors! You lose."


@rps_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("rps", "Play RPS with the bot!", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.Context):
    bot_result = random.choices(["ROCK", "PAPER", "SCISSOR"])

    rpsview = PromptView(timeout=30, autodefer=True)
    rpsview.add_item(RockButton())
    rpsview.add_item(PaperButton())
    rpsview.add_item(ScissorButton())

    prompt = await ctx.respond("Let's play some RPS shall we?", components=rpsview.build())
    msg = await prompt.message()

    rpsview.start(msg)
    await rpsview.wait()

    if hasattr(rpsview, "result"):
        finale = play(rpsview.result, bot_result)
        await ctx.respond(f"{finale}")
    else:
        await ctx.respond(f"**Game has been cancelled due to inactivity.**", delete_after=7)
        await prompt.delete()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(rps_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(rps_plugin)
