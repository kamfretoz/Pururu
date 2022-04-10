import logging
import lightbulb
import hikari
import random
import datetime
from utils.quotes import error_quotes

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
            "CheckFailure": "Command Check Failure, You are not authorized to use this command!",
            "ForbiddenError": "I'm not allowed to perform that action! Permission Denied.",
            "ConcurrencyLimit": "Please wait until the previous command execution has completed!",
        }

async def send_embed(name, code, event, *args):
    message = error_message[name]
    if args:
        message = message.format(*args)
    err = hikari.Embed(description=f"**:warning: {message}**", timestamp=datetime.datetime.now().astimezone(), color=0xFF0000)
    if code:
        err.set_image(f"https://http.cat/{code}.jpg")
    await event.context.respond(content=random.choice(error_quotes), embed=err)

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception
    
    if isinstance(exception, lightbulb.errors.CommandNotFound):
        await send_embed("CommandNotFound", 404, event, exception.invoked_with)
    elif isinstance(exception, lightbulb.errors.MissingRequiredPermission):
        await send_embed("MissingPermissions", 403, event, exception.missing_perms.name)
    elif isinstance(exception, lightbulb.errors.NotEnoughArguments):
        await send_embed("MissingRequiredArgument", 410, event, ", ".join(arg.name for arg in exception.missing_options))
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await send_embed("CommandOnCooldown", 420, event, int(exception.retry_after))
    elif isinstance(exception, lightbulb.errors.BotMissingRequiredPermission):
        await send_embed("BotMissingPermissions", 403, event, exception.missing_perms.name)
    elif isinstance(exception, lightbulb.errors.NotOwner):
        await send_embed("NotOwner", 401, event)
    elif isinstance(exception, lightbulb.errors.ConverterFailure):
        await send_embed("ConversionError", 400, event, exception.option.name)
    elif isinstance(exception, lightbulb.OnlyInGuild):
        await send_embed("NoPrivateMessage", 423, event)
    elif isinstance(exception, lightbulb.errors.NSFWChannelOnly):
        await send_embed("NSFWChannelRequired", 423, event)
    elif isinstance(exception, lightbulb.errors.CheckFailure):
        await send_embed("CheckFailure", 401, event)
    elif isinstance(exception, lightbulb.errors.MaxConcurrencyLimitReached):
        await send_embed("ConcurrencyLimit", 429, event)
    elif isinstance(event.exception.__cause__, hikari.ForbiddenError):
        await send_embed("ForbiddenError", 403, event)
    else:
        if isinstance(event.exception, lightbulb.CommandInvocationError):
            errormsg = hikari.Embed(title=f"🛑 An error occurred with the `{event.context.command.name}` command.", color=0xFF0000, timestamp=datetime.datetime.now().astimezone())
            errormsg.set_image("https://http.cat/500.jpg")
            errormsg.add_field(name="📜 **__Error Log__**:", value=f"```py\n{exception}```")
            await event.context.respond(content=random.choice(error_quotes), embed=errormsg)
            logging.error(event.exception)
            raise(event.exception)
    
def load(bot):
    bot.subscribe(lightbulb.CommandErrorEvent, on_error)
    
def unload(bot):
    bot.unsubscribe(lightbulb.CommandErrorEvent, on_error)
