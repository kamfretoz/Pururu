import asyncio
import hikari
import lightbulb

ANIMALS = {
    "Dog": "🐶",
    "Cat": "🐱",
    "Panda": "🐼",
    "Fox": "🦊",
    "Red Panda": "🐼",
    "Koala": "🐨",
    "Bird": "🐦",
    "Racoon": "🦝",
    "Kangaroo": "🦘",
}

animal_plugin = lightbulb.Plugin("Animal")

@animal_plugin.command()
@lightbulb.command("animal", "Get a fact + picture of a cute animal :3")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def animal(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("animal_select")
        .set_placeholder("Pick an animal")
    )

    for name, emoji in ANIMALS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an animal from the dropdown :3",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=60,
            predicate=lambda e:
                isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU
            )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        async with ctx.bot.d.aio_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(description=res["fact"], colour=0x3B9DFF)
                embed.set_image(res["image"])

                animal = animal.replace("_", " ")

                await msg.edit(
                    f"Here's a {animal} for you! :3", embed=embed, components=[]
                )
            else:
                await msg.edit(
                    f"API returned a {res.status} status :c", components=[]
                )
                
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(animal_plugin)