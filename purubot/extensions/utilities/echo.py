import lightbulb
from hikari.users import User

loader = lightbulb.Loader()


@loader.command
class UserInfo(
    lightbulb.SlashCommand,
    name="userinfo",
    description="Shows the information of a user",
):
    target = lightbulb.user("target", "The target user")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        if self.target is None:
            self.target: User = ctx.user

        created_at = int(self.target.created_at.timestamp())
        joined_at = int(self.target.)

        await ctx.respond(self.user)
