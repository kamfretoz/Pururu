import lightbulb

loader = lightbulb.Loader()


@loader.command
class Echo(lightbulb.SlashCommand, name="echo", description="Repeats the given text"):
    text: str = lightbulb.string("text", "The text to repeat")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(self.text)
