import asyncio
import os

import hikari
import lightbulb

from bot import extensions


if os.name != "nt":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Read the bot token from a text file
with open(os.getenv("TOKEN_FILE", ".token")) as fp:
    token = fp.read().strip()

# Initialise the bot and lightbulb client
bot = hikari.GatewayBot(
    token,
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
client = lightbulb.client_from_app(bot)


@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    # Load the commands
    await client.load_extensions_from_package(extensions, True)
    # Start the client - causing the commands to be synced with discord
    await client.start()
