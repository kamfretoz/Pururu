import lightbulb
from lightbulb.ext import filament

echo_plugin = lightbulb.Plugin("echo", "Is anyone there?")

@echo_plugin.command()
@lightbulb.option("text", "The text you want to repeat", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("echo", "Repeats the text that you have given", aliases=["say"])
@lightbulb.implements(lightbulb.PrefixCommand)
@filament.utils.pass_options
@lightbulb.implements(lightbulb.PrefixCommand)
async def echo(ctx: lightbulb.Context, text) -> None:
    if isinstance(ctx, lightbulb.PrefixContext):
        await ctx.event.message.delete()

    await ctx.respond(text)
    
@echo_plugin.command()
@lightbulb.command("sua", "irma")
@lightbulb.implements(lightbulb.PrefixCommand)
async def sua(ctx: lightbulb.Context) -> None:
    await ctx.respond("irma")

def load(bot):
    bot.add_plugin(echo_plugin)

def unload(bot):
    bot.remove_plugin(echo_plugin)
