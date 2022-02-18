import lightbulb

binary_plugin = lightbulb.Plugin("binary", "Binary Digit conversion tool")

@binary_plugin.command
@lightbulb.command("binary", "converts between binary and ASCII value")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def bin_tool(ctx: lightbulb.Context) -> None:
    pass

@bin_tool.child
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("value", "the value to decode", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("decode", "convert binary to ascii")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def bin_decode(ctx:lightbulb.Context):
    txt = ctx.options.value
    try:
        bin = ''.join([chr(int(txt, 2)) for txt in txt.split()])
    except Exception as e:
        await ctx.respond(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**")
        return
    if len(bin) <= 479:
        await ctx.respond(f"```{bin}```")
    else:
        try:
            await ctx.author.send(f"```{bin}```")
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
            
            
@bin_tool.child
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("value", "the value to encode", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("encode", "convert ASCII to binary")
@lightbulb.implements(lightbulb.SlashSubCommand, lightbulb.PrefixSubCommand)
async def bin_decode(ctx:lightbulb.Context):
    txt = ctx.options.value
    try:
        bin = ' '.join(format(ord(x), 'b') for x in txt)
    except Exception as e:
        await ctx.respond(f"**Error: `{e}`. This probably means the text is malformed. Sorry, you can always try here: http://www.unit-conversion.info/texttools/convert-text-to-binary/#data**")
        return
    if len(bin) <= 479:
        await ctx.respond(f"```fix\n{bin}```")
    else:
        try:
            await ctx.author.send(f"```fix\n{bin}```")
            await ctx.respond(f"**{ctx.author.mention} The output too was too large, so I sent it to your DMs! :mailbox_with_mail:**")
        except Exception:
            await ctx.respond(f"**{ctx.author.mention} There was a problem, and I could not send the output. It may be too large or malformed**")
            
def load(bot) -> None:
    bot.add_plugin(binary_plugin)

def unload(bot) -> None:
    bot.remove_plugin(binary_plugin)
