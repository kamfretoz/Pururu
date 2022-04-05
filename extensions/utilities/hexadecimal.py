import lightbulb

hex_plugin = lightbulb.Plugin("hexadecimal", "68 65 78")

def decode(value: str):
    hex = bytearray.fromhex(value).decode()
    return hex

def encode(value: str):
    hexoutput = " ".join("{:02x}".format(ord(c)) for c in value)
    return hexoutput

@hex_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("value", "the value to decode", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("mode", "the mode of operation", str, required = True, choices=["encode", "decode"])
@lightbulb.command("hex", "convert hex to ascii or vice versa", pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def hexadecimal(ctx:lightbulb.Context, mode: str, value: str):
    try:
        if mode == "decode":
            hex = decode(value)
        else:
            hex = encode(value)
    except Exception as e:
        await ctx.respond(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here**: http://www.unit-conversion.info/texttools/hexadecimal/#data")
        return
    if len(hex) <= 480:
        await ctx.respond(f"```{hex}```")
    else:
        try:
            await ctx.author.send(f"```{hex}```")
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
            
            
def load(bot) -> None:
    bot.add_plugin(hex_plugin)

def unload(bot) -> None:
    bot.remove_plugin(hex_plugin)
