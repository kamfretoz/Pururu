import os
import hikari
import lightbulb
import os

tools_plugin = lightbulb.Plugin("toolbox")
tools_plugin.add_checks(lightbulb.checks.owner_only)

@tools_plugin.command()
@lightbulb.command("crash", "Raise an error", aliases=["dummy", "error"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def crash(ctx: lightbulb.Context) -> None:
    await ctx.respond("Generating an Error Message..")
    raise ValueError("This is a user generated crash")

@tools_plugin.command()
@lightbulb.command("clearterm","clear the output of the console",aliases=["clearconsole", "cc", "cls"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def clear(ctx: lightbulb.Context):
    """Clear the console."""
    if os.name == "nt":
        os.system("cls")
    else:
        try:
            os.system("clear")
        except Exception:
            for _ in range(100):
                print()
    await ctx.respond("Console cleared successfully.")

@tools_plugin.command()
@lightbulb.option("globals", "Whether or not to purge global slash commands from the bot.", hikari.OptionType.BOOLEAN, required = True, default = False)
@lightbulb.option("guild","The ID of the target guild", hikari.OptionType.STRING, required = True)
@lightbulb.command("clear_cmd", "purge all slash commands from specified guild")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def purge_cmd(ctx: lightbulb.Context):
    guild = ctx.options.guild
    await ctx.bot.purge_application_commands(guild, global_commands=ctx.options.globals)
    await ctx.respond("Task Completed Successfully!")

@tools_plugin.command()
@lightbulb.command("extension", "manage an extension")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def extension_manager(ctx:lightbulb.Context):
    pass

@extension_manager.child()
@lightbulb.option("name", "the extension you want to reload", hikari.OptionType.STRING, required=True)
@lightbulb.option("category", "the category of the extension", required = True, choices=["fun", "information", "moderation", "utilities"])
@lightbulb.command("reload", "Reload an extension")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def extension_reload(ctx:lightbulb.Context):
    name = ctx.options.name
    category = ctx.options.category
    await ctx.respond(f"Reloading the extension `{ctx.options.name}`")
    ctx.bot.reload_extensions(f"extensions.{category}.{name}")
    await ctx.edit_last_response(f"Successfully reloaded `{ctx.options.name}`!")


def load(bot):
    bot.add_plugin(tools_plugin)

def unload(bot):
    bot.remove_plugin(tools_plugin)
