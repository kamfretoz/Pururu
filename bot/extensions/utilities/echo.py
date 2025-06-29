import lightbulb
import hikari
import aiohttp
import json

loader = lightbulb.Loader()


@loader.command
class Echo(lightbulb.SlashCommand, name="echo", description="Repeats the given text"):

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, cs: aiohttp.ClientSession) -> None:
        async with cs.get('https://api.adviceslip.com/advice') as resp:
            data = json.loads(await resp.read())
        adv = data["slip"]["advice"]
        emb = hikari.Embed(title="Here's some advice for you :)", description=adv)
        await ctx.respond(embed=emb)
