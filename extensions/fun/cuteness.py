import lightbulb
import hikari
import json
import dotenv
import os
from datetime import datetime

cute_plugin = lightbulb.Plugin("cute", "cuteness filling command!")

# To retrieve KSoft.Si API KEY
dotenv.load_dotenv()
ksoft_key = os.environ.get("KSOFT_API_KEY")

@cute_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.command("cute", "Fills your life with cuteness", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cute(ctx: lightbulb.Context):
        head = {
            "Authorization": ksoft_key
        }
        async with ctx.bot.d.aio_session.get('https://api.ksoft.si/images/random-aww', headers=head) as resp:
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
            raise ValueError(f"⚠ An Error Occured! **{msg.capitalize()}** (Code: {code})")

        emb = hikari.Embed(timestamp=datetime.utcnow())
        emb.set_image(img_url)
        emb.add_field(name="Title", value=f"[{title}]({source})", inline=False)
        emb.add_field(name="Author", value=author)
        emb.add_field(name="Subreddit", value=subreddit)
        emb.add_field(name="Votes", value=f"⬆ {upvotes} Upvotes\n⬇ {downvotes} Downvotes")
        emb.add_field(name="Comments", value=comments)
        emb.add_field(name="Posted on", value=datetime.fromtimestamp( timestamp), inline=False)
        emb.set_footer("Data provided by: KSoft.Si", icon="https://cdn.ksoft.si/images/Logo128.png")

        await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(cute_plugin)

def unload(bot):
    bot.remove_plugin(cute_plugin)
