from pickletools import optimize
import lightbulb
import io
import hikari
from re import match
from PIL import Image
from lightbulb.ext import filament

hex_color_plugin = lightbulb.Plugin("color", "#RGBforLyfe")

@hex_color_plugin.command()
@lightbulb.add_cooldown(3, 1, lightbulb.cooldowns.UserBucket)
@lightbulb.option("colour_code", "HEX Code for the color", hikari.Color, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("color", "Posts color of given hex code", aliases=["getcolor", "colour", "getcolour"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
@filament.utils.pass_options
async def color(ctx: lightbulb.Context, colour_code):
    hex_regex = '^#?(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})$'
    hex_match = match(hex_regex, str(colour_code))
    if hex_match:
        image = Image.new("RGB", (256, 256), colour_code)
        with io.BytesIO() as file:
            image.save(file, "PNG", optimize=True)
            file.seek(0)
            await ctx.respond(f"Colour with hex code: `{colour_code}`", attachment=file)
    else:
        await ctx.respond(f"Invalid Color Code: `{colour_code}`")
def load(bot) -> None:
    bot.add_plugin(hex_color_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(hex_color_plugin)
