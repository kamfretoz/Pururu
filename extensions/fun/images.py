import lightbulb
import hikari


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
@lightbulb.option("user", "the one you want to hug!", hikari.OptionType.USER, required = True)
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
@lightbulb.option("user", "the one you want to snuggles!", hikari.OptionType.USER, required = True)
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
@lightbulb.option("user", "the one you want to kiss!", hikari.OptionType.USER, required = True)
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
@lightbulb.option("user", "the one you want to tickle!", hikari.OptionType.USER, required = True)
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
@lightbulb.option("user", "the one you want to slap!", hikari.OptionType.USER, required = True)
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
@lightbulb.option("user", "the one you want to poke!", hikari.OptionType.USER, required = True)
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
@lightbulb.option("user", "the one you want to cuddle!", hikari.OptionType.USER, required = True)
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
    
def load(bot):
    bot.add_plugin(img_plugin)

def unload(bot):
    bot.remove_plugin(img_plugin)
