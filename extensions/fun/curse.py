import hikari
import lightbulb
import asyncio
import typing
import functools
from lightbulb.ext import tasks

curse_plugin = lightbulb.Plugin("curse", "Get this thing of off me!", include_datastore=True)

# mapping of user_id to task
curse_tasks: typing.Mapping[int, asyncio.Task[None]] = {}

async def inflict_curse(ctx: lightbulb.Context, user: hikari.Member, emoji: hikari.Emoji):
    with ctx.bot.stream(hikari.GuildMessageCreateEvent, timeout=1800).filter(lambda e: e.author.id == user.id) as curse:
        async for event in curse:
            await event.message.add_reaction(emoji)


async def cure_curse(user):
    del curse_tasks[user]

@curse_plugin.command
@lightbulb.add_cooldown(60, 3, lightbulb.GuildBucket)
@lightbulb.option("emoji", "The emoji to use", hikari.Emoji, required=True)
@lightbulb.option("user", "The user to curse", hikari.Member, required=True)
@lightbulb.command("curse", "Curse someone with emoji!", auto_defer=True, pass_options=True, aliases=["santet", "kutuk"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def curse(ctx: lightbulb.Context, user: hikari.Member, emoji: hikari.Emoji):
        if user is None and emoji is None:
            await ctx.respond(embed=hikari.Embed(description="Please specify who to curse and with what emoji!"))
            return

        if emoji is None:
            await ctx.respond(embed=hikari.Embed(description="Please specify what emoji to use!"))
            return

        if user.id == ctx.bot.application.id:
            user = ctx.author
            await ctx.respond(embed=hikari.Embed(description="HA! Nice try! But unfortunately i'm immune to the curse and so the curse goes back to sender!"))
            
        if ctx.author.id in curse_tasks:
            await ctx.respond(
                embed=hikari.Embed(
                    description=f"{user.mention} is already cursed!"
                )
            )
            return
        
        if isinstance(ctx, lightbulb.PrefixCommand):
            await ctx.event.message.add_reaction(emoji)

        task = asyncio.create_task(inflict_curse(ctx, user, emoji))
        task.add_done_callback(functools.partial(cure_curse, ctx.author))

        await ctx.respond(
            embed=hikari.Embed(
                description=f":purple_heart: {user.mention} Has been cursed with {emoji}. The effect will fade away in 30 minutes.",
            )
        )
            
@curse_plugin.command
@lightbulb.add_cooldown(60, 2, lightbulb.UserBucket)
@lightbulb.option("user", "The user to bless", hikari.Member, required=True)
@lightbulb.command("bless", "Cure someone from the curse!", auto_defer=True, pass_options=True, aliases=["ruqyah"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def bless(ctx: lightbulb.Context, user: hikari.Member):
    try:
        curse_plugin.d.cursed_list[user.id]
    except KeyError:
        await ctx.respond(
            embed=hikari.Embed(
                description=f":octagonal_sign: {user.mention} is not cursed.",
            )
        )
        return
        
    task = curse_plugin.d.cursed_list[user.id]["task"]
    id = curse_plugin.d.cursed_list[user.id]["user_id"]
        
    if ctx.author.id == id:
        await ctx.respond(
            embed=hikari.Embed(
                description=":octagonal_sign: You cannot counter-curse yourself",
            )
        )
    elif task is not None:
        task.cancel()
        del curse_plugin.d.cursed_list[user.id]
        await ctx.respond(
            embed=hikari.Embed(
                description=f":green_heart: {user.mention} Has been blessed and the curse had faded away",
            )
        )
        
@tasks.task(h=1, auto_start=True)
async def clear_sniper():
    curse_plugin.d.cursed_list.clear()

def load(bot):
    bot.add_plugin(curse_plugin)

def unload(bot):
    bot.remove_plugin(curse_plugin)
