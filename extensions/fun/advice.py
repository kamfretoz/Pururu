import lightbulb
import hikari
import json

advice_plugin = lightbulb.Plugin("advices", "Some advices that might aid you in your journey of life! :)")

@advice_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("advice", "Send useful advices!.", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def dad(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(f'https://api.adviceslip.com/advice') as resp:
        data = json.loads(await resp.read())
    adv = data["slip"]["advice"]
    emb = hikari.Embed(title="Here's some advice for you :)", description=adv)
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(advice_plugin)

def unload(bot):
    bot.remove_plugin(advice_plugin)
