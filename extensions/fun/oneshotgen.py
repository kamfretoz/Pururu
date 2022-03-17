import lightbulb
import asyncio
import concurrent.futures
from lightbulb.ext import filament
from PIL import Image, ImageFont, ImageDraw
from textwrap import fill
from io import BytesIO
from pathlib import Path

oneshot_plugin = lightbulb.Plugin("oneshot", "OneShot TextBox Generator", include_datastore=True)

oneshot_plugin.d.faces = []

for path in Path("./res/oneshot/faces/").glob("*.png"):
    oneshot_plugin.d.faces.append(path.name[:-4])
    
def image_processing(expression: str, text: str):
    with Image.open("res/oneshot/template.png") as template:
        template = template.convert("RGBA")
        with Image.open("res/oneshot/textboxArrow.png") as arrow:
            arrow = arrow.convert("RGBA")
            template.alpha_composite(arrow, (300, 118))
            with Image.open(f"res/oneshot/faces/{expression}.png") as sprite:
                sprite = sprite.convert("RGBA")
                template.alpha_composite(sprite, (496, 16))
                font = ImageFont.truetype("res/oneshot/font-b.ttf", 24)
                draw = ImageDraw.Draw(template)
                stuff = fill(text ,width=40)
                draw.multiline_text((20, 8), stuff, fill=(255,255,255,255), font=font, align = "left")
                return template

@oneshot_plugin.command()
@lightbulb.add_cooldown(1, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text you want to write", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("expression", "The expression you want Niko to be", str, required=True, choices=oneshot_plugin.d.faces)
@lightbulb.command("oneshot", "Generate a custom OneShot Textbox", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def oneshotgen(ctx: lightbulb.Context, expression, text) -> None:
    loop = asyncio.get_running_loop()
    
    with concurrent.futures.ProcessPoolExecutor() as pool:
        img = await loop.run_in_executor(pool, image_processing, expression, text)
        
    with BytesIO() as image_binary:
        img.save(image_binary, format="PNG")
        image_binary.seek(0)
        await ctx.respond("Here you go!",attachment = image_binary)
    
def load(bot):
    bot.add_plugin(oneshot_plugin)

def unload(bot):
    bot.remove_plugin(oneshot_plugin)
