import hikari
import lightbulb
import base64

base64_plugin = lightbulb.Plugin("base64")

@base64_plugin.command()
@lightbulb.command("base64", "Allows you to encode or decode base64")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def base64_(ctx: lightbulb.Context) -> None:
    pass

@base64_.child()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("input", "the value to decode", type = str, required = True)
@lightbulb.command("decode", "to decode the base64 value")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def base64_decode(ctx: lightbulb.Context) -> None:
    text = ctx.options.input
    try:
        base64_string = text
        base64_bytes = base64_string.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        await ctx.respond(embed=hikari.Embed(description=f"```{sample_string}```"))
    except UnicodeEncodeError:
        await ctx.respond(embed=hikari.Embed(description=f"⚠️ Unable to decode the text, possible unsupported characters are found."))

@base64_.child()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("input", "the text you want to encode", type = str, required = True)
@lightbulb.command("encode", "to encode the ASCII text")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def base64_encode(ctx: lightbulb.Context) -> None:
    sample_string = ctx.options.input
    try:
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        await ctx.respond(embed=hikari.Embed(description=f"```{base64_string}```"))
    except UnicodeEncodeError:
        await ctx.respond(embed=hikari.Embed(description=f"⚠️ Unable to encode the text, possible unsupported characters are found."))

def load(bot) -> None:
    bot.add_plugin(base64_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(base64_plugin)
