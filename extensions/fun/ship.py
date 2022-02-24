import lightbulb
import hikari
import asyncio
import concurrent.futures
from random import randint, choice
from io import BytesIO
from datetime import datetime
from PIL import Image
from utils.masks import ellipse
from lightbulb.ext import filament

ship_plugin = lightbulb.Plugin("ship", "Will it sail or sank?", include_datastore=True)

def image_processing(user1: BytesIO, user2: BytesIO):
    bg = Image.open("res/ship.png")
    bg.convert("RGBA")
    pfp1 = Image.open(user1)
    pfp1.convert("RGBA")
    pfp1 = pfp1.resize((200, 200), reducing_gap=3.0)
    pfp2 = Image.open(user2)
    pfp2.convert("RGBA")
    pfp2 = pfp2.resize((pfp1.size), reducing_gap=3.0)
    
    mask = ellipse(pfp1.size)
    
    bg.paste(pfp1, (30, 30), mask)
    bg.paste(pfp2, (bg.width - pfp1.width - 30, 30), mask)
    
    return bg

@ship_plugin.command()
@lightbulb.add_cooldown(2, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("user2", "The other one you want to ship", hikari.Member, required=True)
@lightbulb.option("user1", "The one you want to ship", hikari.Member, required=True)
@lightbulb.command("ship", "Ship somebody with someone else!", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def ship(ctx: lightbulb.Context, user1, user2) -> None:
    shipnumber = randint(0, 100)
    if 0 <= shipnumber <= 10:
        status = "Really low! {}".format(choice(["Friendzone ;(",
                                                'Just "friends"',
                                                '"Friends"',
                                                "Little to no love ;(",
                                                "There's barely any love ;("]))
    elif 10 <= shipnumber <= 20:
        status = "Low! {}".format(choice(["Still in the friendzone",
                                        "Still in that friendzone ;(",
                                        "There's not a lot of love there... ;("]))
    elif 20 <= shipnumber <= 30:
        status = "Poor! {}".format(choice(["But there's a small sense of romance from one person!",
                                        "But there's a small bit of love somewhere",
                                        "I sense a small bit of love!",
                                        "But someone has a bit of love for someone..."]))
    elif 30 <= shipnumber <= 40:
        status = "Fair! {}".format(choice(["There's a bit of love there!",
                                        "There is a bit of love there...",
                                        "A small bit of love is in the air..."]))
    elif 40 <= shipnumber <= 60:
        status = "Moderate! {}".format(choice(["But it's very one-sided OwO",
                                            "It appears one sided!",
                                            "There's some potential!",
                                            "I sense a bit of potential!",
                                            "There's a bit of romance going on here!",
                                            "I feel like there's some romance progressing!",
                                            "The love is getting there..."]))
    elif 60 <= shipnumber <= 68:
        status = "Good! {}".format(choice(["I feel the romance progressing!",
                                        "There's some love in the air!",
                                        "I'm starting to feel some love!",
                                        "We are definitely getting there!!"]))
    elif shipnumber == 69:
        status = "Nice."
    elif 70 <= shipnumber <= 80:
        status = "Great! {}".format(choice(["There is definitely love somewhere!",
                                            "I can see the love is there! Somewhere...",
                                            "I definitely can see that love is in the air",
                                            "Its getting more and more intense!!"]))
    elif 80 <= shipnumber <= 90:
        status = "Over average! {}".format(choice(["Love is in the air!",
                                                "I can definitely feel the love",
                                                "I feel the love! There's a sign of a match!",
                                                "There's a sign of a match!",
                                                "I sense a match!",
                                                "A few things can be improved to make this a match made in heaven!"]))
    elif 90 <= shipnumber <= 99:
        status = "True love! {}".format(choice(["It's a match!",
                                                "There's a match made in heaven!",
                                                "It's definitely a match!",
                                                "Love is truely in the air!",
                                                "Love is most definitely in the air!"]))
    elif shipnumber == 100:
        status = "Forever lover! {}".format(
            choice(["Forever together and never be apart."]))
    else:
        status = "🤔"
        
    meter = "🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤"
    if shipnumber <= 10:
        meter = "❤🖤🖤🖤🖤🖤🖤🖤🖤🖤"
    elif shipnumber <= 20:
        meter = "❤❤🖤🖤🖤🖤🖤🖤🖤🖤"
    elif shipnumber <= 30:
        meter = "❤❤❤🖤🖤🖤🖤🖤🖤🖤"
    elif shipnumber <= 40:
        meter = "❤❤❤❤🖤🖤🖤🖤🖤🖤"
    elif shipnumber <= 50:
        meter = "❤❤❤❤❤🖤🖤🖤🖤🖤"
    elif shipnumber <= 60:
        meter = "❤❤❤❤❤❤🖤🖤🖤🖤"
    elif shipnumber <= 70:
        meter = "❤❤❤❤❤❤❤🖤🖤🖤"
    elif shipnumber <= 80:
        meter = "❤❤❤❤❤❤❤❤🖤🖤"
    elif shipnumber <= 90:
        meter = "❤❤❤❤❤❤❤❤❤🖤"
    else:
        meter = "❤❤❤❤❤❤❤❤❤❤"

    if shipnumber <= 33:
        shipColor = 0xE80303
    elif 33 < shipnumber < 66:
        shipColor = 0xff6600
    elif 67 < shipnumber < 90:
        shipColor = 0x3be801
    else:
        shipColor = 0xee82ee

    name1letters = user1.username[:round(len(user1.username) / 2)]
    name2letters = user2.username[round(len(user2.username) / 2):]
    shipname = "".join([name1letters, name2letters])
    emb = (hikari.Embed(color=shipColor,
                        title="Love test for:",
                        timestamp=datetime.now().astimezone(),
                        description="**{0}** and **{1}** (**{2}**) {3}".format(user1, user2, shipname, choice([
                            ":sparkling_heart:",
                            ":heart_decoration:",
                            ":heart_exclamation:",
                            ":heartbeat:",
                            ":heartpulse:",
                            ":hearts:",
                            ":blue_heart:",
                            ":green_heart:",
                            ":purple_heart:",
                            ":revolving_hearts:",
                            ":yellow_heart:",
                            ":two_hearts:"]))))
    emb.set_author(name="Shipping Machine!")
    emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
    emb.add_field(name="Status:", value=(status), inline=False)
    emb.add_field(name="Love Meter:", value=meter, inline=False)
    
    user1_asset = user1.avatar_url
    user1_pfp = BytesIO(await user1_asset.read())
    user2_asset = user2.avatar_url
    user2_pfp = BytesIO(await user2_asset.read())
    
    with concurrent.futures.ProcessPoolExecutor() as pool:
        loop = asyncio.get_running_loop()
        img = await loop.run_in_executor(pool, image_processing, user1_pfp, user2_pfp)
        
    with BytesIO() as image_binary:
        img.save(image_binary, format="PNG", optimize=True, quality=80)
        image_binary.seek(0)
        await ctx.respond(embed=emb, attachment=image_binary, content = "Here is the result!")

def load(bot):
    bot.add_plugin(ship_plugin)

def unload(bot):
    bot.remove_plugin(ship_plugin)
