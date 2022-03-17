import lightbulb
import hikari
from lightbulb.ext import filament
from yarl import URL


img_plugin = lightbulb.Plugin("images", "Images manipulation related command")

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("wink", "*wink*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def wink(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://some-random-api.ml/animu/wink') as wink:
        data = await wink.json()
        result = data.get('link')
        embed = hikari.Embed(color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the one you want to hug!", hikari.User , required = True)
@lightbulb.command("hug", "*hugs you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def hugs(ctx: lightbulb.Context, user):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/hug') as hug:
        data = await hug.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"🤗 {ctx.author.mention} hugs {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the one you want to snuggles!", hikari.User , required = True)
@lightbulb.command("snuggle", "*snuggles you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def snug(ctx: lightbulb.Context, user):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/cuddle') as snuggle:
        data = await snuggle.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"🤗 {ctx.author.mention} snuggles {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the one you want to kiss!", hikari.User , required = True)
@lightbulb.command("kiss", "*kisses you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def kiss(ctx: lightbulb.Context, user):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/kiss') as kissy:
        data = await kissy.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"😘 {ctx.author.mention} kisses {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the one you want to tickle!", hikari.User , required = True)
@lightbulb.command("tickle", "*tickles you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def tick(ctx: lightbulb.Context, user):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/tickle') as tickle:
        data = await tickle.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"👐 {ctx.author.mention} tickles {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the one you want to slap!", hikari.User , required = True)
@lightbulb.command("slap", "*slaps you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def slapping(ctx: lightbulb.Context, user):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/slap') as slap:
        data = await slap.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"🤜 {ctx.author.mention} slapped {user.mention}!", color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the one you want to poke!", hikari.User , required = True)
@lightbulb.command("poke", "*pokes you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def poking(ctx: lightbulb.Context, user):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/poke') as poke:
        data = await poke.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"👉 {ctx.author.mention} poked {user.mention}!", color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the one you want to cuddle!", hikari.User , required = True)
@lightbulb.command("pat", "*pats you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def pats(ctx: lightbulb.Context, user):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/pat') as pat:
        data = await pat.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"{ctx.author.mention} gives {user.mention} some headpats!", color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("user", "the horny one!", hikari.User , required = True)
@lightbulb.command("horny", "Horny card for u", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def horny(ctx: lightbulb.Context, user):
    parameters = {
        "avatar" : str(user.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/horny", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    await ctx.respond(embed=em)
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("message", "the text you want to write!", str , required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("member", "the name of the user!", hikari.Member , required = True)
@lightbulb.command("tweet", "create a fake tweet", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def tweet(ctx: lightbulb.Context, member: hikari.Member, message: str):
    parameters = {
        "avatar" : member.avatar_url.url,
        "username" : member.username,
        "displayname" : member.display_name or member.username,
        "comment" : message
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/tweet", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    await ctx.respond(embed=em) # sending the file
    
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("message", "the text you want to write!", str , required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("member", "the name of the user!", hikari.Member , required = True)
@lightbulb.command("ytcomment", "create a youtube comment", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def yt(ctx:lightbulb.Context, member: hikari.Member, message: str):
    parameters = {
        "avatar" : member.avatar_url.url,
        "username" : member.username,
        "comment" : message
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/youtube-comment", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("comrade", "☭", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def comrade(ctx: lightbulb.Context, member):
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/comrade", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("gay", "the gay-laser", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def gay(ctx: lightbulb.Context, member):
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/gay", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("text", "the text you want to write!", str , required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("member", "the name of the user!", hikari.User , required = True)
@lightbulb.command("stupid", "Oh no its stupid", auto_defer = True, aliases = ["sputid"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def stupid(ctx:lightbulb.Context, member, text):
    parameters = {
        "avatar" : str(member.avatar_url),
        "dog" : text
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/its-so-stupid", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("lolipolice", "the police coming to your house", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def lolipolice(ctx: lightbulb.Context, member):
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/lolice", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("simpcard", "this is certified simp moment", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def simpcard(ctx: lightbulb.Context, member):
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/simpcard", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            title=f"what a simp, {member.username}.",
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("jail", "Welcome to the Jail", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def jail(ctx: lightbulb.Context, member):
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/jail", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            title=f"{member.username} has been jailed.",
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("kill", "You Died", auto_defer = True, aliases=["wasted"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def wasted(ctx: lightbulb.Context, member):
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/wasted", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            title=f"{member.username} has died",
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("missionpass", "Mission Passed! Respect++", aliases=["pass"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def passed(ctx: lightbulb.Context, member):
    parameters = {
        "avatar": str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/passed", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            title=f"Mission passed",
            description="Respect +100",
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("member", "the target user!", hikari.User , required = True)
@lightbulb.command("triggered", "TRIGGERED", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def triggered(ctx: lightbulb.Context, member):
    parameters = {
        "avatar": str(member.avatar_url)
    }
    url = URL.build(scheme="https", host="some-random-api.ml", path="/canvas/triggered", query=parameters)
    imageData = hikari.URL(str(url))
    em = hikari.Embed(
            title=f"{member.username} have been triggered!",
            color=0xf1f1f1,
        )
    em.set_image(imageData)
    
    await ctx.respond(embed=em) # sending the file          

def load(bot):
    bot.add_plugin(img_plugin)

def unload(bot):
    bot.remove_plugin(img_plugin)
