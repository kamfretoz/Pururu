import os
import lightbulb
from lightbulb.ext import filament

tools_plugin = lightbulb.Plugin("toolbox", "Authorized Personel Only")
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
@lightbulb.option("globals", "Whether or not to purge global slash commands from the bot.", bool, required = True, default = False)
@lightbulb.option("guild","The ID of the target guild", str, required = True)
@lightbulb.command("clearcmd", "purge all slash commands from specified guild")
@lightbulb.implements(lightbulb.PrefixCommand)
@filament.utils.pass_options
async def purge_cmd(ctx: lightbulb.Context, guild: str, globals: bool):
    await ctx.bot.purge_application_commands(guild, global_commands=globals)
    await ctx.respond("Task Completed Successfully!")

@tools_plugin.command()
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command("extension", "manage an extension")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def extension_manager(ctx:lightbulb.Context):
    pass

@extension_manager.child()
@lightbulb.option("name", "the extension you want to reload", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required = True, choices=["fun", "information", "moderation", "music" ,"utilities"])
@lightbulb.command("reload", "Reload an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
@filament.utils.pass_options
async def extension_reload(ctx:lightbulb.Context):
    name = ctx.options.name
    category = ctx.options.category
    await ctx.respond(f"Reloading the extension `{ctx.options.name}`")
    ctx.bot.reload_extensions(f"extensions.{category}.{name}")
    await ctx.edit_last_response(f"Successfully reloaded `{ctx.options.name}`!")
    
@extension_manager.child()
@lightbulb.option("name", "the extension you want to unload", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required = True, choices=["fun", "information", "moderation", "music" ,"utilities"])
@lightbulb.command("unload", "Unload an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
@filament.utils.pass_options
async def extension_unload(ctx:lightbulb.Context, name: str, category: str):
    await ctx.respond(f"unloading the extension `{name}`")
    ctx.bot.unload_extensions(f"extensions.{category}.{name}")
    await ctx.edit_last_response(f"Successfully unloaded `{name}`!")
    
@extension_manager.child()
@lightbulb.option("name", "the extension you want to load", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required = True, choices=["fun", "information", "moderation", "music" ,"utilities"])
@lightbulb.command("load", "Load an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
@filament.utils.pass_options
async def extension_load(ctx:lightbulb.Context, name: str, category: str):
    await ctx.respond(f"loading the extension `{name}`")
    ctx.bot.load_extensions(f"extensions.{category}.{name}")
    await ctx.edit_last_response(f"Successfully loaded `{name}`!")

def load(bot):
    bot.add_plugin(tools_plugin)

def unload(bot):
    bot.remove_plugin(tools_plugin)
