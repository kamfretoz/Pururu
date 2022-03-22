import os
import aiohttp
import dotenv
import hikari
import lightbulb
import miru
from random import choice
from utils.quotes import statuses

dotenv.load_dotenv()

TOKEN = os.environ["BOT_TOKEN"]
PREFIX = os.environ["PREFIX"]

bot = lightbulb.BotApp(
    TOKEN.strip(),
    default_enabled_guilds=(875986914367385600, 617173140476395542, 535677066138353674, 393724666474135552), # <- Example
    prefix=lightbulb.when_mentioned_or(PREFIX),
    intents=hikari.Intents.ALL,
    help_slash_command=True,
    ignore_bots=True,
    case_insensitive_prefix_commands=True,
    logs={
        "version": 1,
        "incremental": True,
        "loggers": {
            "hikari": {"level": "INFO"},
            "lightbulb": {"level": "INFO"},
        },
    },
)

miru.load(bot)

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()


bot.load_extensions_from("./extensions/", must_exist=True, recursive=True)
bot.load_extensions_from("./meta/", must_exist=True, recursive=True)
bot.load_extensions("lightbulb.ext.filament.exts.superuser")


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name=choice(statuses),
            type=hikari.ActivityType.WATCHING,)
    )
