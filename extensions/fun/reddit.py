import lightbulb
import hikari
import json
import dotenv
import os
from datetime import datetime


subreddit_plugin = lightbulb.Plugin("subreddit", "REEEEEEEEEEEEEEEEEEEEdit")

# To retrieve KSoft.Si API KEY
dotenv.load_dotenv()
ksoft_key = os.environ.get("KSOFT_API_KEY")

@subreddit_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("span", "select range from which to get the images.", hikari.OptionType.STRING, required = False, choices = ["hour", "day", "week", "month", "year", "all"], default = "day")
@lightbulb.option("sub", "the subreddit you want to see", hikari.OptionType.STRING, required = True)
@lightbulb.command("subreddit", "Sends a random weird imagery from subreddit", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def subreddit(ctx: lightbulb.Context):
    reddit = ctx.options.sub
    span = ctx.options.span
    head = {
        "Authorization": ksoft_key
    }
    param = {
        "remove_nsfw": "true",
        "span": span
    }
    async with ctx.bot.d.aio_session.get(f'https://api.ksoft.si/images/rand-reddit/{reddit}', headers=head, params=param) as resp:
        data = json.loads(await resp.read())
    try:
        title = data["title"]
        img_url = data["image_url"]
        source = data["source"]
        subreddit = data["subreddit"]
        upvotes = data["upvotes"]
        downvotes = data["downvotes"]
        comments = data["comments"]
        timestamp = data["created_at"]
        author = data["author"]
    except KeyError:
        code = data["code"]
        msg = data["message"]
        raise ValueError(f"⚠ An Error Occured! {msg.capitalize()} (Code: {code})")
    emb = hikari.Embed(timestamp=datetime.utcnow())
    emb.set_image(img_url)
    emb.add_field(name="Title", value=f"[{title}]({source})", inline=False)
    emb.add_field(name="Author", value=author)
    emb.add_field(name="Subreddit", value=subreddit)
    emb.add_field(
        name="Votes", value=f"⬆ {upvotes} Upvotes\n⬇ {downvotes} Downvotes")
    emb.add_field(name="Comments", value=comments)
    emb.add_field(name="Posted on", value=datetime.fromtimestamp(
        timestamp), inline=False)
    emb.set_footer("Data provided by: KSoft.Si",icon="https://cdn.ksoft.si/images/Logo128.png")
    await ctx.respond(embed=emb)



def load(bot):
    bot.add_plugin(subreddit_plugin)

def unload(bot):
    bot.remove_plugin(subreddit_plugin)
