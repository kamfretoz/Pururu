import asyncio
import concurrent
from io import BytesIO
from textwrap import fill

import lightbulb
from PIL import Image, ImageFont
from pilmoji import Pilmoji

from utils.masks import ellipse

loader = lightbulb.Loader()

font_content = ImageFont.truetype("res/quote/NotoSansCJKjp-Regular.ttf", 18)
font_name = ImageFont.truetype("res/quote/NotoSansCJKjp-Medium.ttf", 20)


def image_processing(pfp: BytesIO, name: str, content: str):
    with Image.new(mode="RGBA", size=(800, 300), color=(0, 0, 0)) as base:
        icon = Image.open(pfp)
        icon.convert("RGBA")
        icon = icon.resize(
            (200, 200), reducing_gap=3.0, resample=Image.Resampling.LANCZOS
        )

        mask = ellipse(icon.size)

        base.paste(icon, (30, 30), mask)

        with Pilmoji(base) as final:
            final.text(
                (250, 100 if len(content) < 100 else 20),
                fill(content, width=60, max_lines=12),
                font=font_content,
                align="left",
            )
            final.text((80, 250), f"{name}", font=font_name, align="center")

    image = BytesIO()
    base.save(image, format="PNG", optimize=True, quality=100)
    image.seek(0)
    return image


@loader.command
class MakeQuote(lightbulb.MessageCommand, name="Create Quote"):
    @lightbulb.invoke
    async def invoke(
        self, ctx: lightbulb.Context, pool: concurrent.futures.ProcessPoolExecutor
    ) -> None:
        pfp = (
            self.target.author.make_avatar_url(
                file_format="WEBP", size=4096, lossless=True
            )
            or self.target.author.default_avatar_url
        )
        user_pfp = BytesIO()

        async with pfp.stream() as reader:
            async for chunk in reader:
                user_pfp.write(chunk)

        loop = asyncio.get_running_loop()
        img = await loop.run_in_executor(
            pool,
            image_processing,
            user_pfp,
            self.target.author.display_name,
            self.target.content.strip(),
        )

        await ctx.respond(attachment=img)
