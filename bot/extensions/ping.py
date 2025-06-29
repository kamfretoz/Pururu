import lightbulb

loader = lightbulb.Loader()


@loader.command
class Ping(lightbulb.SlashCommand, name="ping", description="Checks the bot is alive"):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Pong!")
