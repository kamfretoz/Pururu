import lightbulb
import hikari

dad_plugin = lightbulb.Plugin("dadjokes", "OK Boomer.")

@dad_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("dadjokes", "Send dadjokes.", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def dad(ctx: lightbulb.Context) -> None:
        head = {"Accept": "application/json",
                "User-Agent": "KamFreBOT(Discord BOT) https://github.com/kamfretoz/KamFreBOT"
                }

        async with ctx.bot.d.aio_session.get('https://icanhazdadjoke.com/', headers=head) as resp:
            data = await resp.json()

        jokes = data["joke"]

        emb = hikari.Embed(title="Dad Joke!", description=jokes, color=ctx.author.accent_colour)
        emb.set_thumbnail("https://i.ibb.co/6WjYXsP/dad.jpg")

        await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(dad_plugin)

def unload(bot):
    bot.remove_plugin(dad_plugin)
