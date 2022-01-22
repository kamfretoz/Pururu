import lightbulb

echo_plugin = lightbulb.Plugin("echo")

@echo_plugin.command()
@lightbulb.option("text", "The text you want to repeat", type=str, required=True)
@lightbulb.command("echo", "Repeats the text that you have given", aliases=["say"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)

def load(bot):
    bot.add_plugin(echo_plugin)

def unload(bot):
    bot.remove_plugin(echo_plugin)