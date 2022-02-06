import lightbulb
import hikari
from lightbulb.ext import filament

amiibo_plugin = lightbulb.Plugin("amiibo", "For Nintendo's Amiibo related command")

@amiibo_plugin.command()
@lightbulb.option("query", "The amiibo you want to look up", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("amiibo", "Look up information on Nintendo's Amiibo", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def amiibo(ctx: lightbulb.Context, query) -> None:
    #--First we connect to the Amiibo API and download the Amiibo information--#
    parameters = {
        "name": query
    }
    async with ctx.bot.d.aio_session.get('https://amiiboapi.com/api/amiibo/', params=parameters) as amiibo:
        data = await amiibo.json()
        #--Now we attempt to extract information--#
        try:
            series = data['amiibo'][0]['amiiboSeries']
            character = data['amiibo'][0]['character']
            name = data['amiibo'][0]['name']
            game = data['amiibo'][0]['gameSeries']
            atype = data['amiibo'][0]['type']
            na_release = data['amiibo'][0]['release']['na']
            eu_release = data['amiibo'][0]['release']['eu']
            jp_release = data['amiibo'][0]['release']['jp']
            au_release = data['amiibo'][0]['release']['au']
            image = data['amiibo'][0]['image']
            #--Finally, we format it into a nice little embed--#
            embed = hikari.Embed(
                title=f"Amiibo information for {name} ({series} series)", color=0xd82626)
            embed.add_field(name='Character Represented', value=character)
            embed.add_field(name='Amiibo Series', value=f"{series} series")
            embed.add_field(name='Game of Origin', value=game)
            embed.add_field(name='Type', value=atype)
            embed.add_field(
                name='Released', value=f":flag_us: {na_release}\n:flag_eu: {eu_release}\n:flag_jp: {jp_release}\n:flag_au: {au_release}")
            embed.set_image(image)
            embed.set_thumbnail("https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Amiibo.svg/1024px-Amiibo.svg.png")
            await ctx.respond(embed=embed)
        except KeyError:
            raise ValueError("❌ I couldn't find any Amiibo with that name. Double-check your spelling and try again.")


def load(bot):
    bot.add_plugin(amiibo_plugin)

def unload(bot):
    bot.remove_plugin(amiibo_plugin)
