import os

import aiohttp
import dotenv
import hikari
import lightbulb

dotenv.load_dotenv()

bot = lightbulb.BotApp(
    os.environ["BOT_TOKEN"],
    prefix="x!",
    intents=hikari.Intents.ALL,
    default_enabled_guilds=(875986914367385600,617173140476395542),
    ignore_bots=True,
    logs={
        "version": 1,
        "incremental": True,
        "loggers": {
            "hikari": {"level": "INFO"},
            "hikari.ratelimits": {"level": "TRACE_HIKARI"},
            "lightbulb": {"level": "DEBUG"},
        },
    },
)

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()


bot.load_extensions_from("./extensions/", must_exist=True, recursive=True)
bot.load_extensions_from("./meta/", must_exist=True, recursive=True)


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot.run()
