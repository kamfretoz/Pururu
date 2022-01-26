import lightbulb
import hikari

roast_plugin = lightbulb.Plugin("roast", "Has been roastin since 2011!")

@roast_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "The user you want to roast!", hikari.Member, required=True)
@lightbulb.command("roast", "For all kinds of jokes! (Some might be offensive, be careful.)", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def roast(ctx: lightbulb.Context) -> None:
        member = ctx.options.user
    
        parameters = {
            "lang" : "en",
            "type" : "json"
        }

        async with ctx.bot.d.aio_session.get('https://evilinsult.com/generate_insult.php', params = parameters) as resp:
            
            data = await resp.json()

        insult = data["insult"]

        await ctx.respond(content=f"{member.mention}, {insult}")

def load(bot):
    bot.add_plugin(roast_plugin)

def unload(bot):
    bot.remove_plugin(roast_plugin)
