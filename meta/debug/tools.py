import os
import sys
import lightbulb
import hikari
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
@lightbulb.add_cooldown(3600, 3, lightbulb.GlobalBucket)
@lightbulb.option("url", "The Avatar's URL you want to use!", str, required = False)
@lightbulb.command("setbotavatar","Set the bot's avatar", aliases=["botava"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand)
@filament.utils.pass_options
async def setbotavatar(ctx: lightbulb.Context, url: str):
    if ctx.attachments:
        url = ctx.attachments[0].url
    elif url is None:
        await ctx.respond("Please specify an avatar url if you did not attach a file")
        return
    try:
        await ctx.bot.rest.edit_my_user(avatar=str(hikari.URL(url)))
    except Exception as e:
        await ctx.respond("Unable to change avatar: {}".format(e))
        return
    await ctx.respond(":eyes:")
    
@tools_plugin.command()
@lightbulb.add_cooldown(3600, 3, lightbulb.GlobalBucket)
@lightbulb.option("name", "The name you want to change to!", str, required = True)
@lightbulb.command("setbotname","Set the bot's name", aliases=["botname"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand)
@filament.utils.pass_options
async def setbotname(ctx: lightbulb.Context, name: str):
    try:
        await ctx.bot.rest.edit_my_user(username=name)
    except Exception as e:
        await ctx.respond("Unable to change the name: {}".format(e))
        return
    await ctx.respond(f"I now identify as `{name}`")
    

@tools_plugin.command()
@lightbulb.option("globals", "Whether or not to purge global slash commands from the bot.", bool, required = True, default = False)
@lightbulb.option("guild","The ID of the target guild", hikari.Snowflake, required = True)
@lightbulb.command("clearcmd", "purge all slash commands from specified guild")
@lightbulb.implements(lightbulb.PrefixCommand)
@filament.utils.pass_options
async def purge_cmd(ctx: lightbulb.Context, guild: hikari.Snowflake, globals: bool):
    await ctx.bot.purge_application_commands(guild, global_commands=globals)
    await ctx.respond("Task Completed Successfully!")

@tools_plugin.command()
@lightbulb.add_checks(lightbulb.checks.owner_only)
@lightbulb.command("extension", "manage an extension")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def extension_manager():
    pass

@extension_manager.child
@lightbulb.option("name", "the extension you want to reload", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required = True, choices=["fun", "information", "moderation", "music" ,"utilities"])
@lightbulb.command("reload", "Reload an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
@filament.utils.pass_options
async def extension_reload(ctx:lightbulb.Context, name: str, category: str):
    ctx.bot.reload_extensions(f"extensions.{category}.{name}")
    await ctx.respond(f"Successfully reloaded `{name}`!")
    
@extension_manager.child
@lightbulb.option("name", "the extension you want to unload", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required = True, choices=["fun", "information", "moderation", "music" ,"utilities"])
@lightbulb.command("unload", "Unload an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
@filament.utils.pass_options
async def extension_unload(ctx:lightbulb.Context, name: str, category: str):
    ctx.bot.unload_extensions(f"extensions.{category}.{name}")
    await ctx.respond(f"Successfully unloaded `{name}`!")
    
@extension_manager.child
@lightbulb.option("name", "the extension you want to load", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("category", "the category of the extension", str, required = True, choices=["fun", "information", "moderation", "music" ,"utilities"])
@lightbulb.command("load", "Load an extension", inherit_checks=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
@filament.utils.pass_options
async def extension_load(ctx:lightbulb.Context, name: str, category: str):
    ctx.bot.load_extensions(f"extensions.{category}.{name}")
    await ctx.respond(f"Successfully loaded `{name}`!")
    
@tools_plugin.command()
@lightbulb.command("shutdown", "Power Off the bot.", aliases=["poweroff", "shutdown", "kms", "altf4", "fuckmylife", "fml", "fuckoff"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def shutdown(ctx: lightbulb.Context) -> None:
    await ctx.respond("Shutting Down...")
    await ctx.bot.close()
    sys.exit()

@tools_plugin.command()
@lightbulb.command("restart", "Restart the bot.")
@lightbulb.implements(lightbulb.PrefixCommand)
async def restart(ctx: lightbulb.Context) -> None:
    await ctx.respond("Restarting...")
    await ctx.bot.close()
    os.system("clear")
    os.execv(sys.executable, ['python3'] + sys.argv)

def load(bot):
    bot.add_plugin(tools_plugin)

def unload(bot):
    bot.remove_plugin(tools_plugin)
