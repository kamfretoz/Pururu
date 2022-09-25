import lightbulb
import hikari

urban_plugin = lightbulb.Plugin("urban", "Urban Dictionary related command!")

@urban_plugin.command()
@lightbulb.option("definition", "The definition you want to look up", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("urban", "Look up urban dictionary for the given word!", auto_defer = True, pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def urban(ctx: lightbulb.Context, definition) -> None:
    #--First we connect to Urban Dictionary's API and get the results--#
    parameters = {
        "term": definition
    }
    async with ctx.bot.d.aio_session.get(f'http://api.urbandictionary.com/v0/define', params=parameters) as r:
        #--Now we decode the JSON and get the variables, truncating definitions and examples if they are longer than 900 characters due to Discord API limitations and replacing example with None if blank--#
        try:
            result = await r.json()
            word = result['list'][0]['word']
            url = result['list'][0]['permalink']
            upvotes = result['list'][0]['thumbs_up']
            downvotes = result['list'][0]['thumbs_down']
            author = result['list'][0]['author']
            definition = result['list'][0]['definition']
            definition = definition.replace('[', '')
            definition = definition.replace(']', '')
            if len(definition) > 900:
                definition = definition[0:901]
                definition = f"{definition}[...]({url})"
            example = result['list'][0]['example']
            example = example.replace('[', '')
            example = example.replace(']', '')
            if len(example) > 900:
                example = example[0:901]
                example = f"{example}[...]({url})"
            if len(example) < 1:
                example = None
        except (IndexError, KeyError):
            await ctx.respond(":x: Sorry, I couldn't find that word. Check your spelling and try again.")
            return
        embed = hikari.Embed(
            title=f":notebook: Urban Dictionary Definition for {word}", description=definition, url=url, color=0x8253c3)
        if example == None:
            pass
        else:
            embed.add_field(name="Example:",
                            value=example, inline=False)
        embed.set_footer(
            text=f"Author: {author} - 👍️ {str(upvotes)} - 👎️ {str(downvotes)}")
        await ctx.respond(content='', embed=embed)
    
def load(bot):
    bot.add_plugin(urban_plugin)

def unload(bot):
    bot.remove_plugin(urban_plugin)
