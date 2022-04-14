from functools import lru_cache
import lightbulb
import asyncio
import hikari
from PIL import Image, ImageFont, ImageDraw
from textwrap import fill
from io import BytesIO
from pathlib import Path
from rapidfuzz import fuzz, process

oneshot_plugin = lightbulb.Plugin("oneshot", "OneShot TextBox Generator")

@lru_cache(maxsize=100)
def get_expression():
    faces = []
    for path in Path("./res/oneshot/faces/").glob("*.png"):
        faces.append(path.name[:-4])
    return faces
    
font = ImageFont.truetype("res/oneshot/font-b.ttf", 24)
    
def image_processing(expression: str, text: str):
    with Image.open("res/oneshot/template.png") as template:
        template = template.convert("RGBA")
        with Image.open("res/oneshot/textboxArrow.png") as arrow:
            arrow = arrow.convert("RGBA")
            template.alpha_composite(arrow, (300, 118))
            with Image.open(f"res/oneshot/faces/{expression}.png") as sprite:
                sprite = sprite.convert("RGBA")
                template.alpha_composite(sprite, (496, 16))
                draw = ImageDraw.Draw(template)
                stuff = fill(text ,width=40)
                draw.multiline_text((20, 8), stuff, fill=(255,255,255,255), font=font, align = "left")
                
                img = BytesIO()
                template.save(img, format="PNG", quality = 100, optimize = True)
                img.seek(0)
                return img

@oneshot_plugin.command()
@lightbulb.add_cooldown(1, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text you want to write", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("face", "The expression you want Niko to be", str, required=True, autocomplete=True)
@lightbulb.command("oneshot", "Generate a custom OneShot Textbox", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def oneshotgen(ctx: lightbulb.Context, face: str, text: str) -> None:
    loop = asyncio.get_running_loop()
    img = await loop.run_in_executor(ctx.bot.d.process_pool, image_processing, face, text)
        
    await ctx.respond("Here you go!", attachment = img)
    
@oneshotgen.autocomplete("face")
async def face_autocomplete(input: hikari.AutocompleteInteractionOption, interaction: hikari.AutocompleteInteraction):
    result = process.extract(input.value, get_expression(), scorer=fuzz.QRatio, limit=5)
    
    if len(result) == 0:
        return "Could not find anything. Sorry."
    
    return [r[0] for r in result]
    
def load(bot):
    bot.add_plugin(oneshot_plugin)

def unload(bot):
    bot.remove_plugin(oneshot_plugin)
