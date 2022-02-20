import lightbulb
import hikari
from lightbulb.ext import filament
from bs4 import BeautifulSoup

kym_plugin = lightbulb.Plugin("knowyourmeme", "Find information about a meme!")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

@kym_plugin.command()
@lightbulb.option("query", "The meme you want to look up", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("knowyourmeme", "Look up information on memes!", auto_defer = True, aliases=["kym"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def kym(ctx: lightbulb.Context, query: str) -> None:
    
    PARAMETERS = {
    'q': query
    }

    async with ctx.bot.d.aio_session.get('http://knowyourmeme.com/search', headers=HEADERS, params=PARAMETERS) as resp:
        text1 = await resp.read()
        soup1 = BeautifulSoup(text1.decode('utf-8'), 'html5lib')
        list1 = soup1.findAll("a", href=True)
    async with ctx.bot.d.aio_session.get('http://knowyourmeme.com' + list1[135]['href'], headers=HEADERS, params=PARAMETERS) as resp2:
        text2 = await resp2.read()
        try:
            soup2 = BeautifulSoup(text2.decode('utf-8'), 'html5lib')  # parsing it
            title = soup2.find('meta', attrs={"property": "og:title"})['content'] # finding the title
            desc = soup2.find('meta', attrs={"property": "og:description"})['content'] # finding the description
            imageurl = soup2.find('meta', attrs={"property": "og:image"})['content']  # finding image url
            siteurl = soup2.find('meta', attrs={"property": "og:url"})['content']  # finding site url
        except TypeError:
            raise ValueError("Query not found")
        
        emb = hikari.Embed(title=title, description=desc)
        emb.add_field("More Information", f"[Click Here.]({siteurl})")
        emb.set_image(imageurl)
    
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(kym_plugin)

def unload(bot):
    bot.remove_plugin(kym_plugin)
