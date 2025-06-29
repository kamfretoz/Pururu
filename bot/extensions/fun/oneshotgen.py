import concurrent.futures
from functools import lru_cache
import lightbulb
import concurrent
import asyncio
import hikari
from PIL import Image, ImageFont, ImageDraw
from textwrap import fill
from io import BytesIO
from pathlib import Path
from rapidfuzz import fuzz, process

loader = lightbulb.Loader()


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
                stuff = fill(text, width=40)
                draw.multiline_text(
                    (20, 8), stuff, fill=(255, 255, 255, 255), font=font, align="left"
                )

                img = BytesIO()
                template.save(img, format="PNG", quality=100, optimize=True)
                img.seek(0)
                return img

@loader.command
class OneshotGen(
    lightbulb.SlashCommand,
    name="oneshotgen",
    description="OneShot TextBox Generator"
):
    @lightbulb.invoke
    async def invoke(
        self, ctx: lightbulb.Context, pool: concurrent.futures.ProcessPoolExecutor
    ) -> None:
        face = lightbulb.string(
            "face", "The expression you want to use", autocomplete=face_autocomplete
        )
        text = lightbulb.string("text", "The text for the dialog box")

        loop = asyncio.get_running_loop()
        img = await loop.run_in_executor(pool, image_processing, face, text)

        await ctx.respond("Here you go!", attachment=img)


async def face_autocomplete(ctx: lightbulb.AutocompleteContext[str]):
    result: list = process.extract(
        ctx.focused.value, get_expression(), scorer=fuzz.QRatio, limit=5
    )

    if len(result) == 0:
        return "Could not find anything. Sorry."

    return [r[0] for r in result]
