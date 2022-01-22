import lightbulb
import hikari
import random
import datetime
from extras.quotes import error_quotes

error_message = {
            "CommandNotFound": "`{}` is an invalid command!",
            "MissingPermissions": "You dont have `{}` permission to run that command!",
            "MissingRequiredArgument": "You are missing required arguments: `{}`, Please refer to the help menu for more information.",
            "CommandOnCooldown": "That command is on cooldown. Please try again after `{}` seconds.",
            "BotMissingPermissions": "I don't have required permission `{}` to complete that command.",
            "NotOwner": "You are not my owner!",
            "ConversionError": "Converter failed for `{}`.",
            "NoPrivateMessage": "This command cannot be used in DMs!",
            "NSFWChannelRequired": "You can only use this command on channels that are marked as NSFW.",
            "CheckFailure": "Command Check Failure, You are not authorized to use this command!"
        }

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        print(f"Ignoring exception in command {event.context.command.name}")
        
        errormsg = hikari.Embed(title=f"🛑 An error occurred with the `{event.context.command.name}` command.", description=f"`{random.choice(error_quotes)}`" ,color=0xFF0000, timestamp=datetime.datetime.now().astimezone())
        errormsg.set_image("https://http.cat/500.jpg")
        await event.context.respond(embed=errormsg)
        await event.context.respond(f"📜 **__Error Log:__**:\n```py\n{event.exception.__cause__}```")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    async def send_embed(name, code: int ,*args):
        message = error_message[name]
        if args:
            message = message.format(*args)
        err = hikari.Embed(description=f"**:warning: {message}**", timestamp=datetime.datetime.now().astimezone(), color=0xFF0000)
        if code:
            err.set_image(f"https://http.cat/{code}.jpg")
        await event.context.respond(content=f"{random.choice(error_quotes)}", embed=err)
    
    if isinstance(exception, lightbulb.errors.CommandNotFound):
        await send_embed("CommandNotFound", 404 ,exception.invoked_with)
    elif isinstance(exception, lightbulb.errors.MissingRequiredPermission):
        await send_embed("MissingPermissions", 403 ,exception.missing_perms)
    elif isinstance(exception, lightbulb.errors.NotEnoughArguments):
        await send_embed("MissingRequiredArgument", 410 ,exception.missing_options)
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await send_embed("CommandOnCooldown", 429 ,int(exception.retry_after))
    elif isinstance(exception, lightbulb.errors.BotMissingRequiredPermission):
        await send_embed("BotMissingPermissions", 403 ,exception.missing_perms)
    elif isinstance(exception, lightbulb.errors.NotOwner):
        await send_embed("NotOwner", 401)
    elif isinstance(exception, lightbulb.errors.ConverterFailure):
        await send_embed("ConversionError", 400 ,exception.option)
    elif isinstance(exception, lightbulb.OnlyInGuild):
        await send_embed("NoPrivateMessage", 423)
    elif isinstance(exception, lightbulb.errors.NSFWChannelRequired):
        await send_embed("NSFWChannelRequired", 423)
    elif isinstance(exception, lightbulb.errors.CheckFailure):
        await send_embed("CheckFailure", 401)
    
def load(bot):
    bot.subscribe(lightbulb.CommandErrorEvent, on_error)
    
def unload(bot):
    bot.unsubscribe()
