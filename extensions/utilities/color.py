import lightbulb
import io
import hikari
from PIL import Image

hex_color_plugin = lightbulb.Plugin("color", "#RGBforLyfe")

@hex_color_plugin.command()
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.option("colour_code", "HEX Code for the color", hikari.Color, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("color", "Posts color of given hex code", aliases=["getcolor", "colour", "getcolour"], pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def color(ctx: lightbulb.Context, colour_code: str):
    image = Image.new("RGB", (256, 256), colour_code)
    with io.BytesIO() as file:
        image.save(file, "PNG")
        file.seek(0)
        await ctx.respond(f"Colour with hex code: `{colour_code}`", attachment=file)

def load(bot) -> None:
    bot.add_plugin(hex_color_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(hex_color_plugin)
