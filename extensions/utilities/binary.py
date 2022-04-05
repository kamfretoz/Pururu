import lightbulb

binary_plugin = lightbulb.Plugin("binary", "Binary Digit conversion tool")

def decode(value: str):
    txt = ''.join([chr(int(value, 2)) for value in value.split()])
    return txt

def encode(value: str):
    bin = ' '.join(format(ord(x), 'b') for x in value)
    return bin

@binary_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("value", "the value to decode on encode", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("mode", "Convert Binary to ASCII or vice versa", str, required = True, choices=["encode", "decode"])
@lightbulb.command("binary", "convert binary to ascii", pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def binary(ctx:lightbulb.Context, mode: str, value: str):
    try:
        if mode == "encode":
            bin = encode(value)
        else:
            bin = decode(value)
    except Exception as e:
        await ctx.respond(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**")
        return
    if len(bin) <= 480:
        await ctx.respond(f"```{bin}```")
    else:
        try:
            await ctx.author.send(f"```{bin}```")
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
            
def load(bot) -> None:
    bot.add_plugin(binary_plugin)

def unload(bot) -> None:
    bot.remove_plugin(binary_plugin)
