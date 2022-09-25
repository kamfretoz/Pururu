import lightbulb
import hikari
pokedex_plugin = lightbulb.Plugin("pokedex", "Pokeom Query Lookup tool")

@pokedex_plugin.command()
@lightbulb.option("pokemon", "The name of the pokemon you want to look up", str, required=True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("pokedex", "Access Pokédex database of Information", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pokedex(ctx: lightbulb.Context, pokemon) -> None:
    #--Some Pokemon with several forms are named differently on the API, so if one of those Pokemon are specified, we replace the query with the correct name--#
    pkmn = {
        'meloetta': 'Meloetta - Aria Forme',
        'keldeo': 'Keldeo - Ordinary Form',
        'burmy': 'Burmy - Plant Cloak',
        'wormadam': 'Wormadam - Plant Cloak',
        'cherrim': 'Cherrim - Overcast Form',
        'giratina': 'Giratina - Altered Forme',
        'shaymin': 'Shaymin - Land Forme',
        'basculin': 'Basculin - Red-Striped Form',
        'deerling': 'Deerling - Spring Form',
        'tornadus': 'Tornadus - Incarnate Forme',
        'thundurus': 'Thundurus - Incarnate Forme',
        'landorus': 'Landorus - Incarnate Forme',
        'flabebe': 'Flabébé',
        'zygarde': 'Zygarde - Complete Forme',
        'hoopa': 'Hoopa Confined',
        'oricorio': 'Oricorio - Baile Style',
        'lycanroc': 'Lycanroc - Midday Form',
        'wishiwashi': 'Wishiwashi - Solo Form',
        'minior': 'Minior - Meteor Form',
        'mimikyu': 'Mimikyu - Disguised Form',
    }.get(pokemon.lower(), pokemon)

    #--First we connect to the Pokedex API and download the Pokedex entry--#
    async with ctx.bot.d.aio_session.get(f'https://pokeapi.glitch.me/v1/pokemon/{pkmn}') as dex_entry:
        data = await dex_entry.json()
        #--Now we attempt to extract information--#
        for x in data:
            try:
                pkmn_name = x['name']
                pkmn_no = x['number']
                pkmn_desc = x['description']
                pkmn_img = x['sprite']
                pkmn_height = x['height']
                pkmn_weight = x['weight']
                pkmn_species = x['species']
                pkmn_type1 = x['types'][0]
                pkmn_gen = str(x['gen'])
                pkmn_ability1 = x['abilities']['normal'][0]
                #--Detect if Pokemon has a second ability--#
                try:
                    pkmn_ability2 = x['abilities']['normal'][1]
                except IndexError:
                    pkmn_ability2 = None
                #--Detect if Pokemon has a hidden ability--#
                try:
                    pkmn_hiddenability = x['abilities']['hidden'][0]
                except IndexError:
                    pkmn_hiddenability = None
                #--Detect if Pokemon has a second type--#
                try:
                    pkmn_type2 = x['types'][1]
                except IndexError:
                    pkmn_type2 = None
                #--Finally, we format it into a nice little embed--#
                embed = hikari.Embed(title=f"Pokédex information for {pkmn_name} (#{pkmn_no})", description=pkmn_desc, color=0xd82626)
                embed.add_field(name='Height', value=pkmn_height)
                embed.add_field(name='Weight', value=pkmn_weight)
                embed.add_field(name='Species', value=pkmn_species)
                #--Detect if type2 is defined--#
                if pkmn_type2 == None:
                    embed.add_field(name='Type', value=pkmn_type1)
                else:
                    embed.add_field(name='Types', value=f"{pkmn_type1}, {pkmn_type2}")
                #--Detect if ability2 and hiddenability defined--#
                if pkmn_ability2 == None:
                    if pkmn_hiddenability == None:
                        embed.add_field(name='Ability', value=pkmn_ability1)
                    else:
                        embed.add_field(name='Abilities', value=f"{pkmn_ability1};\n**Hidden:** {pkmn_hiddenability}")
                else:
                    if pkmn_hiddenability == None:
                        embed.add_field(name='Abilities', value=f"{pkmn_ability1}, {pkmn_ability2}")
                    else:
                        embed.add_field(name='Abilities', value=f"{pkmn_ability1}, {pkmn_ability2};\n**Hidden:** {pkmn_hiddenability}")
                embed.add_field(name='Generation Introduced', value=f"Gen {pkmn_gen}")
                embed.set_thumbnail(pkmn_img)
                await ctx.respond(embed=embed)
            except (KeyError, TypeError):
                raise ValueError(":x: I couldn't find any Pokémon with that name. Double-check your spelling and try again.")

def load(bot):
    bot.add_plugin(pokedex_plugin)

def unload(bot):
    bot.remove_plugin(pokedex_plugin)
