import lightbulb
import hikari
import io


img_plugin = lightbulb.Plugin("images", "Images manipulation related command")

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
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
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the one you want to hug!", hikari.User , required = True)
@lightbulb.command("hug", "*hugs you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def hugs(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/hug') as hug:
        user = ctx.options.user
        data = await hug.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"🤗 {ctx.author.mention} hugs {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the one you want to snuggles!", hikari.User , required = True)
@lightbulb.command("snuggle", "*snuggles you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def snug(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/cuddle') as snuggle:
        user = ctx.options.user
        data = await snuggle.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"🤗 {ctx.author.mention} snuggles {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the one you want to kiss!", hikari.User , required = True)
@lightbulb.command("kiss", "*kisses you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def kiss(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/kiss') as kissy:
        user = ctx.options.user
        data = await kissy.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"😘 {ctx.author.mention} kisses {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the one you want to tickle!", hikari.User , required = True)
@lightbulb.command("tickle", "*tickles you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def tick(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/tickle') as tickle:
        user = ctx.options.user
        data = await tickle.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"👐 {ctx.author.mention} tickles {user.mention}!",  color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the one you want to slap!", hikari.User , required = True)
@lightbulb.command("slap", "*slaps you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def slapping(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/slap') as slap:
        user = ctx.options.user
        data = await slap.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"🤜 {ctx.author.mention} slapped {user.mention}!", color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the one you want to poke!", hikari.User , required = True)
@lightbulb.command("poke", "*pokes you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def poking(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/poke') as poke:
        user = ctx.options.user
        data = await poke.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"👉 {ctx.author.mention} poked {user.mention}!", color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the one you want to cuddle!", hikari.User , required = True)
@lightbulb.command("pat", "*pats you*", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pats(ctx: lightbulb.Context):
    async with ctx.bot.d.aio_session.get('https://nekos.life/api/v2/img/pat') as pat:
        user = ctx.options.user
        data = await pat.json()
        result = data.get('url')
        embed = hikari.Embed(
            description=f"{ctx.author.mention} gives {user.mention} some headpats!", color=0x8253c3)
        embed.set_image(result)
        await ctx.respond(embed=embed)
        
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the horny one!", hikari.User , required = True)
@lightbulb.command("horny", "Horny card for u", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def horny(ctx: lightbulb.Context):
    mem = ctx.options.user
    parameters = {
        "avatar" : str(mem.avatar_url)
    }
    
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/horny', params = parameters) as af:
        if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            fp.seek(0)
            em = hikari.Embed(
                    color=0xf1f1f1,
                )
            em.set_image(fp)
            await ctx.respond(embed=em)
        else:
            await ctx.respond('No horny :(')
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("text", "the text you want to write!", str , required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "the name of the user!", hikari.User , required = True)
@lightbulb.command("tweet", "create a fake tweet", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def tweet(ctx:lightbulb.Context):
    member = ctx.options.user
    message = ctx.options.text
    parameters = {
        "avatar" : str(member.avatar_url),
        "username" : member.username,
        "displayname" : member.display_name or member.username,
        "comment" : message
    }
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/tweet', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            imageData.seek(0)
            em = hikari.Embed(
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            await ctx.respond(attachment=em) # sending the file
    
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("text", "the text you want to write!", str , required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "the name of the user!", hikari.User , required = True)
@lightbulb.command("ytcomment", "create a youtube comment", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def yt(ctx:lightbulb.Context):
    member = ctx.options.user
    message = ctx.options.text
    parameters = {
        "avatar" : str(member.avatar_url),
        "username" : member.username,
        "comment" : message
    }
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/youtube-comment', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            imageData.seek(0)
            em = hikari.Embed(
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("comrade", "☭", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def comrade(ctx: lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/comrade', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("gay", "the gay-laser", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def gay(ctx: lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/gay', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("text", "the text you want to write!", str , required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("user", "the name of the user!", hikari.User , required = True)
@lightbulb.command("stupid", "Oh no its stupid", auto_defer = True, aliases = ["sputid"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def stupid(ctx:lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url),
        "dog" : ctx.options.text
    }

    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/its-so-stupid', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("lolipolice", "the police coming to your house", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def lolipolice(ctx: lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/lolice', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("simpcard", "this is certified simp moment", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def simpcard(ctx: lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/simpcard', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    title=f"what a simp, {member.username}.",
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("jail", "Welcome to the Jail", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def jail(ctx: lightbulb.Context):
    member = ctx.options.user

    parameters = {
        "avatar" : str(member.avatar_url)
    }

    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/jail', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    title=f"{member.username} have been jailed.",
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("kill", "You Died", auto_defer = True, aliases=["wasted"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def wasted(ctx: lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/wasted', params=parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    title=f"{member.username} has died",
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file

@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("missionpass", "Mission Passed! Respect++", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def passed(ctx: lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url)
    }

    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/passed', params = parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    title=f"Mission passed",
                    description="Respect +100",
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file
            
@img_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user", "the target user!", hikari.User , required = True)
@lightbulb.command("triggered", "TRIGGERED", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def triggered(ctx: lightbulb.Context):
    member = ctx.options.user
    parameters = {
        "avatar" : str(member.avatar_url)
    }
    async with ctx.bot.d.aio_session.get(f'https://some-random-api.ml/canvas/triggered', params = parameters) as resp:
            imageData = io.BytesIO(await resp.read()) # read the image/bytes
            em = hikari.Embed(
                    title=f"{member.name} have been triggered!",
                    color=0xf1f1f1,
                )
            em.set_image(imageData)
            
            await ctx.respond(embed=em) # sending the file          

def load(bot):
    bot.add_plugin(img_plugin)

def unload(bot):
    bot.remove_plugin(img_plugin)
