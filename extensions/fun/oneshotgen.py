import lightbulb
from PIL import Image, ImageFont, ImageDraw
from textwrap import fill
from io import BytesIO
from pathlib import Path

oneshot_plugin = lightbulb.Plugin("oneshot", "OneShot TextBox Generator", include_datastore=True)

oneshot_plugin.d.faces = []

for path in Path("./res/oneshot/faces/").glob("*.png"):
    oneshot_plugin.d.faces.append(path.name[:-4])

@oneshot_plugin.command()
@lightbulb.add_cooldown(1, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("text", "The text you want to write", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("expression", "The expression you want Niko to be", str, required=True, choices=oneshot_plugin.d.faces)
@lightbulb.command("oneshot", "Generate a custom OneShot Textbox", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def oneshotgen(ctx: lightbulb.Context) -> None:
    text = ctx.options.text
    expr = ctx.options.expression
    with Image.open("res/oneshot/template.png") as template:
        template = template.convert("RGBA")
        with Image.open("res/oneshot/textboxArrow.png") as arrow:
            arrow = arrow.convert("RGBA")
            template.alpha_composite(arrow, (300, 118))
            with Image.open(f"res/oneshot/faces/{expr}.png") as sprite:
                sprite = sprite.convert("RGBA")
                template.alpha_composite(sprite, (496, 16))
                font = ImageFont.truetype("res/oneshot/font-b.ttf", 24)
                draw = ImageDraw.Draw(template)
                stuff = fill(text ,width=40)
                draw.multiline_text((20, 8), stuff, fill=(255,255,255,255), font=font, align = "left")
                with BytesIO() as image_binary:
                    template.save(image_binary, format="PNG")
                    image_binary.seek(0)
                    await ctx.respond("Here you go!",attachment = image_binary)
    
def load(bot):
    bot.add_plugin(oneshot_plugin)

def unload(bot):
    bot.remove_plugin(oneshot_plugin)
