import lightbulb
import hikari
import dotenv
import json
import os
import pytemperature
from datetime import datetime
from math import trunc

weather_plugin = lightbulb.Plugin("weather")

@weather_plugin.command()
@lightbulb.option("city", "the city you want to check", hikari.OptionType.STRING, required=True)
@lightbulb.command("weather", "See the weather of a given city", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def weather(ctx: lightbulb.Context) -> None:
    city = ctx.options.city
    
    # To retrieve the API KEY
    dotenv.load_dotenv()
    key = os.environ.get("WEATHER_API_KEY")
    # https://stackoverflow.com/a/7490772 https://www.windfinder.com/wind/windspeed.htm
    def degToCompass(deg):
        val = int((deg/22.5)+.5)
        arr = [
            "North (N)",
            "North-Northeast (NNE)",
            "Northeast (NE)",
            "East-Northeast (ENE)",
            "East (E)",
            "East-Southeast (ESE)",
            "Southeast (SE)",
            "South-Southeast (SSE)",
            "South (S)",
            "South-Southwest (SSW)",
            "Southwest (SW)",
            "West-Southwest (WSW)",
            "West (W)",
            "West-Northwest (WNW)",
            "Northwest (NW)",
            "North-Northwest (NNW)"
        ]
        return arr[(val % 16)]
    def metertokilometer(meter):  # https://www.asknumbers.com/meters-to-km.aspx
        km = meter * 0.001
        trc = trunc(km)
        return trc
    def mpstokmh(mtr):  # https://www.mathworksheets4kids.com/solve/speed/conversion2.php
        mul = mtr * 18
        div = mul / 5
        trc = trunc(div)
        return trc
    # In Meter/second https://www.windfinder.com/wind/windspeed.htm
    def wind_condition(wind_speed):
        if wind_speed >= 0 and wind_speed <= 0.2:
            return "Calm"
        elif wind_speed >= 0.2 and wind_speed <= 1.5:
            return "Light Air"
        elif wind_speed >= 1.5 and wind_speed <= 3.3:
            return "Light Breeze"
        elif wind_speed >= 3.3 and wind_speed <= 5.4:
            return "Gentle Breeze"
        elif wind_speed >= 5.4 and wind_speed <= 7.9:
            return "Moderate Breeze"
        elif wind_speed >= 7.9 and wind_speed <= 10.7:
            return "Fresh Breeze"
        elif wind_speed >= 10.7 and wind_speed <= 13.8:
            return "Strong Breeze"
        elif wind_speed >= 13.8 and wind_speed <= 17.1:
            return "Near Gale"
        elif wind_speed >= 17.1 and wind_speed <= 20.7:
            return "Gale"
        elif wind_speed >= 20.7 and wind_speed <= 24.4:
            return "Severe Gale"
        elif wind_speed >= 24.4 and wind_speed <= 28.4:
            return "Strong Storm"
        elif wind_speed >= 28.4 and wind_speed <= 32.6:
            return "Violent Storm"
        elif wind_speed >= 32.6:
            return "Hurricane"
    try:
        parameters = {
            "q": city,
            "appid": key,
            "units": "metric"
        }
        async with ctx.bot.d.aio_session.get("http://api.openweathermap.org/data/2.5/weather", params=parameters) as resp:
            data = json.loads(await resp.read())
        
        code = data["cod"]
        if code != 200:
            msg = data.message
            if code == 404:
                await ctx.respond(embed=hikari.Embed(description="City cannot be found!"))
                return
            elif code == 401:
                await ctx.respond(embed=hikari.Embed(description="Invalid API Key!"))
                return
            else:
                await ctx.respond(embed=hikari.Embed(description=f"An Error Occured! `{msg.capitalize()}` (Code: `{code}`)"))
                return

        cityname = data["name"]
        countryid = data["sys"]["country"]
        country_flags = f":flag_{countryid.lower()}:"
        status = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        timezone_offset = data["timezone"]
        clouds = data["clouds"]["all"]
        lon = data["coord"]["lon"]
        lat = data["coord"]["lat"]
        temp_c = data["main"]["temp"]
        feels_c = data["main"]["feels_like"]
        t_min_c = data["main"]["temp_min"]
        t_max_c = data["main"]["temp_max"]
        temp_f = pytemperature.c2f(temp_c)
        feels_f = pytemperature.c2f(feels_c)
        t_min_f = pytemperature.c2f(t_min_c)
        t_max_f = pytemperature.c2f(t_max_c)
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        vis = data["visibility"]
        wind = data["wind"]["speed"]
        wind_degree = data["wind"]["deg"]
        wind_direction = degToCompass(wind_degree)
        icon = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    except IndexError:
        await ctx.respond(embed=hikari.Embed(description="⚠ An Error Occured while parsing the data."))
        return
    except KeyError:
        await ctx.respond(embed=hikari.Embed(description="⚠ An Error Occured while parsing the data."))
        return
    colours = ""
    if temp_c > 36:
        colours = hikari.Colour(0xFF0000)
    elif temp_c > 28:
        colours = hikari.Colour(0xFFFF00)
    elif temp_c > 16:
        colours = hikari.Colour(0x26D935)
    elif temp_c > 8:
        colours = hikari.Colour(0x006BCE)
    elif temp_c > 2:
        colours = hikari.Colour(0xB4CFFA)
    elif temp_c <= 2:
        colours = hikari.Colour(0x0000FF)
    else:
        colours = hikari.Colour(0x36393E)
    calculated_sunrise = datetime.fromtimestamp(sunrise + timezone_offset)
    calculated_sunset = datetime.fromtimestamp(sunset + timezone_offset)
    embed = hikari.Embed(title="Weather Information",timestamp=datetime.now().astimezone(), color=colours)
    embed.set_thumbnail(icon)
    embed.set_footer("Data provided by: OpenWeatherMap.org")
    embed.add_field(name="🏙 City", value=cityname, inline=False)
    embed.add_field(name="🏳 Country",value=f"{countryid} {country_flags}", inline=False)
    embed.add_field(name="🌻 Weather", value=status, inline=False)
    embed.add_field(name="ℹ Condition",value=description.title(), inline=False)
    embed.add_field(name="🌐 Longitude", value=lon, inline=True)
    embed.add_field(name="🌐 Latitude", value=lat, inline=True)
    embed.add_field(name="🌄 Sunrise",value=f"{calculated_sunrise} (UTC)", inline=True)
    embed.add_field(name="🌇 Sunset",value=f"{calculated_sunset} (UTC)", inline=True)
    embed.add_field(name="🌡 Current Temperature",value=f"{temp_c} °C ({temp_f} °F)", inline=True)
    embed.add_field(name="🌡 Feels Like",value=f"{feels_c} °C ({feels_f} °F)", inline=True)
    embed.add_field(name="🌡 Min Temperature",value=f"{t_min_c} °C ({t_min_f} °F)", inline=True)
    embed.add_field(name="🌡 Max Temperature",value=f"{t_max_c} °C ({t_max_f} °F)", inline=True)
    embed.add_field(name="☁ Cloudiness", value=f"{clouds}%", inline=True)
    embed.add_field(name="🍃Atmospheric Pressure",value=f"{pressure} hPa", inline=True)
    embed.add_field(name="🌬 Humidity", value=f"{humidity}%", inline=True)
    embed.add_field(name="👁️ Visibility",value=f"{vis} Meter ({metertokilometer(vis)} KM)", inline=True)
    embed.add_field(name="💨 Wind Speed", value=f"{wind} m/sec | {mpstokmh(wind)} km/h ({wind_condition(wind)})", inline=True)
    embed.add_field(name="🧭 Wind Direction",value=f"{wind_degree}° {wind_direction}", inline=True)
    
    await ctx.respond(embed=embed)


def load(bot):
    bot.add_plugin(weather_plugin)

def unload(bot):
    bot.remove_plugin(weather_plugin)
