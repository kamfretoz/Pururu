import lightbulb
from io import BytesIO

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
@lightbulb.add_cooldown(2, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("text", "The text you want to write", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("character", "The character you want to pick", str, required=True, choices = undertale_plugin.d.chars)
@lightbulb.command("undertale", "Allows you to create Undertale Textbox")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def undertale(ctx: lightbulb.Context) -> None:
    text = ctx.options.text
    chara = ctx.options.character
    
    await ctx.respond("Loading... Please Wait!")
    parameters = {
        "message": text,
        "character": chara
    }

    async with ctx.bot.d.aio_session.get(f"https://demirramon.com/utgen.png", params=parameters) as resp:
        image_data = await resp.read()
    img = BytesIO(image_data)
    img.seek(0)
    await ctx.edit_last_response("Here you go!",attachment = img)


def load(bot):
    bot.add_plugin(undertale_plugin)

def unload(bot):
    bot.remove_plugin(undertale_plugin)
