import lightbulb
import asyncio
from io import BytesIO
from utils.masks import ellipse
from textwrap import fill, shorten
from PIL import Image, ImageFont
from pilmoji import Pilmoji

def image_processing(pfp: BytesIO, name: str , content: str, ):
    with Image.new(mode = "RGBA", size = (700, 256), color = (21, 22 ,24)) as base:
        icon = Image.open(pfp)
        icon.convert("RGBA")
        icon = icon.resize((200, 200), reducing_gap=3.0, resample=Image.ANTIALIAS)
        
        mask = ellipse(icon.size)
        
        base.paste(icon, (30, 30), mask)
        
        if len(content) > 50:
            size = 20
        elif len(content) > 100:
            size = 16
        elif len(content) > 200:
            size = 14
        elif len(content) > 250:
            size = 12
        else:
            size = 24
    
        font_content = ImageFont.truetype("res/quote/PTSans-Regular.ttf", size)
        font_name = ImageFont.truetype("res/quote/PTSans-BoldItalic.ttf", 24)
        
        if len(content) > 256:
            content = shorten(content, width=250, placeholder=" ... [DATA_EXPUNGED]")
        
        text = fill(content, width=42)
        
        with Pilmoji(base) as final:
            final.text((250, 20), text, fill=(255,255,255,255), font=font_content, align = "left")
            final.text((250, 200), f" — {name}", fill=(255,255,255,255), font=font_name, align = "center")
    
    image = BytesIO()
    base.save(image, format="PNG", optimize=True, quality=100)
    image.seek(0)
    return image
        

aquote_plugin = lightbulb.Plugin("makequote", "Say wha?", include_datastore=True)

@aquote_plugin.command()
@lightbulb.add_cooldown(2, 3, lightbulb.UserBucket)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.MessageCommand)
@lightbulb.set_help(text="Please pick a message by replying to them whilst running this command")
@lightbulb.command("makequote", "Create a quote from someone's message", auto_defer = True, aliases=["mq"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def makequote(ctx: lightbulb.Context) -> None:
    if ctx.event.message.referenced_message is None:
        await ctx.respond("❌ You haven't picked any message to create a quote from. **Please pick a message by replying to them whilst running this command**.")
        return

    reply = ctx.event.message.referenced_message

    name = reply.author.username
    pfp = reply.author.avatar_url
    content = reply.content
    
    if content is None:
        content = ""
    
    user_pfp = BytesIO()
    
    async with pfp.stream() as reader:
        async for chunk in reader:
            user_pfp.write(chunk)
    
    loop = asyncio.get_running_loop()
    img = await loop.run_in_executor(ctx.bot.d.process_pool, image_processing, user_pfp, name, content)

    await ctx.respond(attachment=img, content = "Here is the quote!")

def load(bot):
    bot.add_plugin(aquote_plugin)

def unload(bot):
    bot.remove_plugin(aquote_plugin)
