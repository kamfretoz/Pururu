import lightbulb
import hikari
from lightbulb.ext import filament

dict_plugin = lightbulb.Plugin("dictionary", "*turns to next page*")

@dict_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("word", "The text you want to define", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("define", "Look up the definition of a word", aliases=["def", "dictionary"], auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def dictionary(ctx: lightbulb.Context, word) -> None:
    try:
        #--Connect to unofficial Google Dictionary API and get results--#
        async with ctx.bot.d.aio_session.get(f'https://api.dictionaryapi.dev/api/v1/entries/en/{word}') as r:
            #--Now we decode the JSON and get the variables, replacing them with None if they fail to define--#
            result = await r.json()
            word = result[0]['word']
            try:
                origin = result[0]['origin']
            except KeyError:
                origin = None
            try:
                noun_def = result[0]['meaning']['noun'][0]['definition']
            except KeyError:
                noun_def = None
            try:
                noun_eg = result[0]['meaning']['noun'][0]['example']
            except KeyError:
                noun_eg = None
            try:
                verb_def = result[0]['meaning']['verb'][0]['definition']
            except KeyError:
                verb_def = None
            try:
                verb_eg = result[0]['meaning']['verb'][0]['example']
            except KeyError:
                verb_eg = None
            try:
                prep_def = result[0]['meaning']['preposition'][0]['definition']
            except KeyError:
                prep_def = None
            try:
                prep_eg = result[0]['meaning']['preposition'][0]['example']
            except KeyError:
                prep_eg = None
            try:
                adverb_def = result[0]['meaning']['adverb'][0]['definition']
            except KeyError:
                adverb_def = None
            try:
                adverb_eg = result[0]['meaning']['adverb'][0]['example']
            except KeyError:
                adverb_eg = None
            try:
                adject_def = result[0]['meaning']['adjective'][0]['definition']
            except KeyError:
                adject_def = None
            try:
                adject_eg = result[0]['meaning']['adjective'][0]['example']
            except KeyError:
                adject_eg = None
            try:
                pronoun_def = result[0]['meaning']['pronoun'][0]['definition']
            except KeyError:
                pronoun_def = None
            try:
                pronoun_eg = result[0]['meaning']['pronoun'][0]['example']
            except KeyError:
                pronoun_eg = None
            try:
                exclaim_def = result[0]['meaning']['exclamation'][0]['definition']
            except KeyError:
                exclaim_def = None
            try:
                exclaim_eg = result[0]['meaning']['exclamation'][0]['example']
            except KeyError:
                exclaim_eg = None
            try:
                poss_determ_def = result[0]['meaning']['possessive determiner'][0]['definition']
            except KeyError:
                poss_determ_def = None
            try:
                poss_determ_eg = result[0]['meaning']['possessive determiner'][0]['example']
            except KeyError:
                poss_determ_eg = None
            try:
                abbrev_def = result[0]['meaning']['abbreviation'][0]['definition']
            except KeyError:
                abbrev_def = None
            try:
                abbrev_eg = result[0]['meaning']['abbreviation'][0]['example']
            except KeyError:
                abbrev_eg = None
            try:
                crossref_def = result[0]['meaning']['crossReference'][0]['definition']
            except KeyError:
                crossref_def = None
            try:
                crossref_eg = result[0]['meaning']['crossReference'][0]['example']
            except KeyError:
                crossref_eg = None
            embed = hikari.Embed(
                title=f":blue_book: Google Definition for {word}", color=0x8253c3)
            #--Then we add see if the variables are defined and if they are, those variables to an embed and send it back to Discord--#
            if origin == None:
                pass
            else:
                embed.add_field(name="Origin:", value=origin, inline=False)
            if noun_def == None:
                pass
            else:
                if noun_eg == None:
                    embed.add_field(
                        name="As a Noun:", value=f"**Definition:** {noun_def}", inline=False)
                else:
                    embed.add_field(
                        name="As a Noun:", value=f"**Definition:** {noun_def}\n**Example:** {noun_eg}", inline=False)
            if verb_def == None:
                pass
            else:
                if verb_eg == None:
                    embed.add_field(
                        name="As a Verb:", value=f"**Definition:** {verb_def}", inline=False)
                else:
                    embed.add_field(
                        name="As a Verb:", value=f"**Definition:** {verb_def}\n**Example:** {verb_eg}", inline=False)
            if prep_def == None:
                pass
            else:
                if prep_eg == None:
                    embed.add_field(
                        name="As a Preposition:", value=f"**Definition:** {prep_def}", inline=False)
                else:
                    embed.add_field(
                        name="As a Preposition:", value=f"**Definition:** {prep_def}\n**Example:** {prep_eg}", inline=False)
            if adverb_def == None:
                pass
            else:
                if adverb_eg == None:
                    embed.add_field(
                        name="As an Adverb:", value=f"**Definition:** {adverb_def}", inline=False)
                else:
                    embed.add_field(
                        name="As a Adverb:", value=f"**Definition:** {adverb_def}\n**Example:** {adverb_eg}", inline=False)
            if adject_def == None:
                pass
            else:
                if adject_eg == None:
                    embed.add_field(
                        name="As an Adjective:", value=f"**Definition:** {adject_def}", inline=False)
                else:
                    embed.add_field(
                        name="As an Adjective:", value=f"**Definition:** {adject_def}\n**Example:** {adject_eg}", inline=False)
            if pronoun_def == None:
                pass
            else:
                if pronoun_eg == None:
                    embed.add_field(
                        name="As a Pronoun:", value=f"**Definition:** {pronoun_def}", inline=False)
                else:
                    embed.add_field(
                        name="As a Pronoun:", value=f"**Definition:** {pronoun_def}\n**Example:** {pronoun_eg}", inline=False)
            if exclaim_def == None:
                pass
            else:
                if exclaim_eg == None:
                    embed.add_field(
                        name="As an Exclamation:", value=f"**Definition:** {exclaim_def}", inline=False)
                else:
                    embed.add_field(
                        name="As an Exclamation:", value=f"**Definition:** {exclaim_def}\n**Example:** {exclaim_eg}", inline=False)
            if poss_determ_def == None:
                pass
            else:
                if poss_determ_eg == None:
                    embed.add_field(name="As a Possessive Determiner:",
                                    value=f"**Definition:** {poss_determ_def}", inline=False)
                else:
                    embed.add_field(name="As a Possessive Determiner:",
                                    value=f"**Definition:** {poss_determ_def}\n**Example:** {poss_determ_eg}", inline=False)
            if abbrev_def == None:
                pass
            else:
                if abbrev_eg == None:
                    embed.add_field(
                        name="As an Abbreviation:", value=f"**Definition:** {abbrev_def}", inline=False)
                else:
                    embed.add_field(
                        name="As an Abbreviation:", value=f"**Definition:** {abbrev_def}\n**Example:** {abbrev_eg}", inline=False)
            if crossref_def == None:
                pass
            else:
                if crossref_eg == None:
                    embed.add_field(
                        name="As a Cross-Reference:", value=f"**Definition:** {crossref_def}", inline=False)
                else:
                    embed.add_field(
                        name="As a Cross-Reference:", value=f"**Definition:** {crossref_def}\n**Example:** {crossref_eg}", inline=False)
            await ctx.respond(embed=embed)
    except:
        #--Send error message if command fails, as it's assumed a definition isn't found--#
        await ctx.respond(content=":x: Sorry, I couldn't find that word. Check your spelling and try again.")

def load(bot):
    bot.add_plugin(dict_plugin)

def unload(bot):
    bot.remove_plugin(dict_plugin)
