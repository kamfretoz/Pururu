import hikari
import lightbulb

meme_plugin = lightbulb.Plugin("meme")

@meme_plugin.command()
@lightbulb.command("meme", "Get a funni meme")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def meme(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        "https://meme-api.herokuapp.com/gimme"
    ) as response:
        res = await response.json()

        if response.ok and res["nsfw"] != True:
            link = res["postLink"]
            title = res["title"]
            img_url = res["url"]

            embed = hikari.Embed(colour=0x3B9DFF)
            embed.set_author(name=title, url=link)
            embed.set_image(img_url)

            await ctx.respond(embed)

        else:
            await ctx.respond(
                "Could not fetch a meme :c", flags=hikari.MessageFlag.EPHEMERAL
            )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(meme_plugin)