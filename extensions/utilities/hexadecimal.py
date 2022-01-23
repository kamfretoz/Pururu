import lightbulb
import hikari

hex_plugin = lightbulb.Plugin("hexadecimal")

@hex_plugin.command
@lightbulb.command("hex", "converts between hexadecimal and ASCII value")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def hex_tool(ctx: lightbulb.Context) -> None:
    pass

@hex_tool.child
@lightbulb.option("value", "the value to decode", hikari.OptionType.STRING, required = True)
@lightbulb.command("decode", "convert hex to ascii")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def hex_decode(ctx:lightbulb.Context):
    txt = ctx.options.value
    try:
        hex = bytearray.fromhex(txt).decode()
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
            
@hex_tool.child
@lightbulb.option("value", "the value to decode", hikari.OptionType.STRING, required = True)
@lightbulb.command("encode", "convert ascii to hex")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def hex_encode(ctx:lightbulb.Context):
    txt = ctx.options.value
    try:
        hexoutput = " ".join("{:02x}".format(ord(c)) for c in txt)
    except Exception as e:
        await ctx.respond(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/hexadecimal/#data**")
    if len(hexoutput) <= 479:
        await ctx.respond(f"```fix\n{hexoutput}```")
    else:
        try:
            await ctx.author.send(f"```fix\n{hexoutput}```")
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
            
            
def load(bot) -> None:
    bot.add_plugin(hex_plugin)

def unload(bot) -> None:
    bot.remove_plugin(hex_plugin)
