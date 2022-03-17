import lightbulb
import hikari
import qrcode
from io import BytesIO
from lightbulb.ext import filament

qr_plugin = lightbulb.Plugin("qr", "A QR Code Maker")

@qr_plugin.command()
@lightbulb.command("qr", "Creates a QR Code", aliases=["qrcode"])
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def qr(ctx: lightbulb.Context) -> None:
    pass

@qr.child()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("data", "The text you want to encode", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("create", "Encodes a text into a QR Code", aliases=["make"])
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
@filament.utils.pass_options
async def qr_maker(ctx: lightbulb.Context, data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    img = qr.make_image(fill_color="black", back_color="white")
    with BytesIO() as file:
            img.save(file, "PNG")
            file.seek(0)
            await ctx.respond(f"Here is your QR Code:", attachment=file)
            
@qr.child()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("temporary", "set if you want the member joined to be temporary", bool, required=False, default = False)
@lightbulb.option("max_use", "The limit of the invite usage", int, required=False, default=0)
@lightbulb.option("max_time", "The duration of the invite (in seconds, defaults to 1 day which is 86400 seconds)", int, required=False, default=86400)
@lightbulb.option("channel", "The channel you want to pick", hikari.TextableGuildChannel, required=True)
@lightbulb.command("invite", "Encodes an invite into a QR Code", aliases=["inv"])
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
@filament.utils.pass_options
async def qr_invite(ctx: lightbulb.Context, channel, max_use, max_time, temporary):
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    link = await ctx.bot.rest.create_invite(channel, max_uses=max_use, max_age=max_time ,temporary=temporary)
    qr.add_data(link)
    img = qr.make_image(fill_color="black", back_color="white")
    with BytesIO() as file:
            img.save(file, "PNG")
            file.seek(0)
            await ctx.respond(f"Here is your QR Code:", attachment=file)

def load(bot):
    bot.add_plugin(qr_plugin)

def unload(bot):
    bot.remove_plugin(qr_plugin)
