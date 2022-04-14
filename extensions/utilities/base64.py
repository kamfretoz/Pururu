import hikari
import lightbulb
import base64

base64_plugin = lightbulb.Plugin("base64", "Base64 Conversion tool")

def encode(value: str):
    sample_string = value
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string
    

def decode(value: str):
    base64_string = value
    base64_bytes = base64_string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string


@base64_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("input", "the value to decode", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("mode", "the conversion", str, required = True, choices=["encode", "decode"])
@lightbulb.command("base64", "to decode or encode a base64 value", pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def b64(ctx: lightbulb.Context, mode:str, input: str) -> None:
    try:
        if mode == "decode":
            direction = "Base64 🡪 ASCII"
            final = decode(input)
        else:
            direction = "Base64 🡨 ASCII"
            final = encode(input)
        await ctx.respond(embed=hikari.Embed(title =f"{direction} Conversion:", description=f"```{final}```"))
    except UnicodeEncodeError:
        await ctx.respond(embed=hikari.Embed(description=f"⚠️ Unable to decode the text, possible unsupported characters are found."))

def load(bot) -> None:
    bot.add_plugin(base64_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(base64_plugin)
