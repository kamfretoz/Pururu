import asyncio
import hikari

rest = hikari.RESTApp()

TOKEN = hikari.UNDEFINED
GUILD_ID = hikari.UNDEFINED

async def main():
    async with rest.acquire(TOKEN, hikari.TokenType.BOT) as client:
        application = await client.fetch_application()
        await client.set_application_commands(application.id, (), guild=GUILD_ID)

asyncio.run(main())
