import asyncio
import concurrent.futures
import aiohttp
import os
import concurrent

import hikari
import lightbulb

from purubot import extensions
from utils import const


if os.name != "nt":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Read the bot token from a text file
with open(os.getenv("TOKEN_FILE", ".token")) as fp:
    token = fp.read().strip()

# Initialise the bot and lightbulb client
Pururu = hikari.GatewayBot(
    token,
    cache_settings=const.CACHE,
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
client = lightbulb.client_from_app(Pururu, default_enabled_guilds=const.GUILDS)

Pururu.subscribe(hikari.StoppingEvent, client.stop)


@Pururu.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    client.di.registry_for(lightbulb.di.Contexts.DEFAULT).register_factory(
        aiohttp.ClientSession, lambda: aiohttp.ClientSession()
    )

    client.di.registry_for(lightbulb.di.Contexts.DEFAULT).register_factory(
        concurrent.futures.ProcessPoolExecutor, lambda: concurrent.futures.ProcessPoolExecutor()
    )

    # Load the commands
    await client.load_extensions_from_package(extensions, recursive=True)
    # Start the client - causing the commands to be synced with discord
    await client.start()
