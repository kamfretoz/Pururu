import os
import aiohttp
import dotenv
import hikari
import lightbulb

dotenv.load_dotenv()

bot = lightbulb.BotApp(
    os.environ["BOT_TOKEN"],
    default_enabled_guilds=(875986914367385600),
    prefix=os.environ["PREFIX"],
    intents=hikari.Intents.ALL,
    ignore_bots=True,
    help_slash_command=True,
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
        status=hikari.Status.IDLE,
        activity=hikari.Activity(
            name="from the distance...",
            type=hikari.ActivityType.WATCHING,)
    )