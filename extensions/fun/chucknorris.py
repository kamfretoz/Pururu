import lightbulb
import hikari

chuck_plugin = lightbulb.Plugin("chucknorris", "You Didn't run this command, Chuck Norris throw this command at your face.")

@chuck_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.command("chucknorris", "Chuck Norris Jokes.", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def chuck(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get('https://api.chucknorris.io/jokes/random') as resp:
        data = await resp.json()
    joke = data["value"]
    icon = data["icon_url"]
    emb = hikari.Embed(
        description=joke, color=0x8B0000)
    emb.set_thumbnail(icon)
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(chuck_plugin)

def unload(bot):
    bot.remove_plugin(chuck_plugin)
