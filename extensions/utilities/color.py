import lightbulb
import io
from re import match
from PIL import Image

hex_color_plugin = lightbulb.Plugin("color", "#RGBforLyfe")

@hex_color_plugin.command()
@lightbulb.add_cooldown(3, 1, lightbulb.cooldowns.UserBucket)
@lightbulb.option("color_code", "HEX Code for the color", type = str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("color", "Posts color of given hex code", aliases=["getcolor", "colour", "getcolour"])
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def color(ctx: lightbulb.Context):
    colour_codes = ctx.options.color_code
    colour_codes = colour_codes.split()
    size = (60, 80) if len(colour_codes) > 1 else (200, 200)
    for colour_code in colour_codes:
        hex_regex = '^#?(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})$'
        hex_match = match(hex_regex, colour_code)
        if hex_match:
            if not colour_code.startswith("#"):
                colour_code = "#" + colour_code
            image = Image.new("RGB", size, colour_code)
            with io.BytesIO() as file:
                image.save(file, "PNG")
                file.seek(0)
                await ctx.respond(f"Colour with hex code: `{colour_code}`", attachment=file)
        else:
            await ctx.respond(f"Invalid Color Code: `{colour_codes}`")
def load(bot) -> None:
    bot.add_plugin(hex_color_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(hex_color_plugin)
