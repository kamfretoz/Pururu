import lightbulb
import hikari
from lightbulb.ext import filament
from yarl import URL

undertale_plugin = lightbulb.Plugin("undertale", "Generates custom undertale textbox!", include_datastore=True)

undertale_plugin.d.chars = [
    "frisk",
    "flowey",
    "toriel",
    "napsta",
    "sans",
    "papyrus",
    "undyne",
    "temmie",
    "alphys",
    "mettaton",
    "mettaton-ex",
    "muffet",
    "asgore",
    "omega-flowey",
    "asriel",
    "chara",
    "wd-gaster",
    "kris",
    "susie",
    "ralsei",
    "noelle",
    "lancer",
    "gevil",
    "queen",
    "spamton"
]

@undertale_plugin.command()
@lightbulb.add_cooldown(2, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text you want to write", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("character", "The character you want to pick", str, required=True, choices = undertale_plugin.d.chars)
@lightbulb.command("undertale", "Allows you to create Undertale Textbox")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def undertale(ctx: lightbulb.Context, character, text) -> None:
    parameters = {
        "message": text,
        "character": character
    }
    url = URL.build(scheme="https", host="demirramon.com", path="/utgen.png", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    await ctx.respond("Here you go!", embed=em)


def load(bot):
    bot.add_plugin(undertale_plugin)

def unload(bot):
    bot.remove_plugin(undertale_plugin)
