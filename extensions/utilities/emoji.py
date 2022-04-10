import hikari
import lightbulb
import re
from lightbulb.utils import pag

emoji_plugin = lightbulb.Plugin("emoji", "Emoji related utilities.")

static_re = re.compile(r"<:([^:]+):(\d+)>")
animated_re = re.compile(r"<a:([^:]+):(\d+)>")

@emoji_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("Steal Emoji", "Steal emojis from a message.", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.MessageCommand)
async def steal(ctx: lightbulb.Context, target: hikari.Message):
    animated = animated_re.findall(target.content)
    static = static_re.findall(target.content)

    if not static and not animated:
        await ctx.respond(":x: No custom emojis could be found on that message...", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    paginator = pag.StringPaginator(max_lines=10)
    paginator.add_line(f"Emoji looted from: {target.make_link(ctx.get_guild())}")
    
    for name, id in static:
        paginator.add_line(f" ➡ :{name}: https://cdn.discordapp.com/emojis/{id}.png")
    for name, id in animated:
        paginator.add_line(f" ➡ :{name}: https://cdn.discordapp.com/emojis/{id}.gif (animated)")
    
    total = len(animated) + len(static)
    
    for pages in paginator.build_pages():
        await ctx.author.send(pages)
        
    await ctx.respond(f"✅ Congratulations! **You have looted {total} emojis!**", flags=hikari.MessageFlag.EPHEMERAL, delete_after=5)
    

def load(bot):
    bot.add_plugin(emoji_plugin)

def unload(bot):
    bot.remove_plugin(emoji_plugin)
