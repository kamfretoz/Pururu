import json

import aiohttp
import hikari
import lightbulb

loader = lightbulb.Loader()


@loader.command
class Advice(
    lightbulb.SlashCommand,
    name="advice",
    description="Some advices that might aid you in your journey of life! :)",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context, cs: aiohttp.ClientSession) -> None:
        async with cs.get("https://api.adviceslip.com/advice") as resp:
            data = json.loads(await resp.read())
        adv = data["slip"]["advice"]
        emb = hikari.Embed(title="Here's some advice for you :)", description=adv)
        await ctx.respond(embed=emb)
