import lightbulb

loader = lightbulb.Loader()

@loader.command
class Advice(lightbulb.SlashCommand, name="advice", description="Some advices that might aid you in your journey of life! :)"):
    text: str = lightbulb.string("text", "The text to repeat")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(self.text)
