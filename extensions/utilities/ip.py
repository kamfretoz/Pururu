import lightbulb
import hikari
import json
import datetime
from re import match
from lightbulb.ext import filament

ip_plugin = lightbulb.Plugin("ip", "IP Adress Query Lookup")
ip_regex = '^(?!^0\.)(?!^10\.)(?!^100\.6[4-9]\.)(?!^100\.[7-9]\d\.)(?!^100\.1[0-1]\d\.)(?!^100\.12[0-7]\.)(?!^127\.)(?!^169\.254\.)(?!^172\.1[6-9]\.)(?!^172\.2[0-9]\.)(?!^172\.3[0-1]\.)(?!^192\.0\.0\.)(?!^192\.0\.2\.)(?!^192\.88\.99\.)(?!^192\.168\.)(?!^198\.1[8-9]\.)(?!^198\.51\.100\.)(?!^203.0\.113\.)(?!^22[4-9]\.)(?!^23[0-9]\.)(?!^24[0-9]\.)(?!^25[0-5]\.)(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))$'

@ip_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("address", "The ip you want to analyze", str, required=True)
@lightbulb.command("ip", "Lookup information of an IP Adress", aliases=["ipaddr"], auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def ip_finder(ctx: lightbulb.Context, address) -> None:
    
    ip_result = match(ip_regex, address)
    if ip_result:
        async with ctx.bot.d.aio_session.get(f'https://ipapi.co/{address}/json/') as resp:
            
            data = json.loads(await resp.read())
            
        ipaddr = data["ip"]
        city = data["city"] or "Unknown"
        region = data["region"] or "Unknown"
        region_code = data["region_code"] or "Unknown"
        country = data["country"] or "Unknown"
        country_name = data["country_name"] or "Unknown"
        country_code_iso3 = data["country_code_iso3"] or "Unknown"
        continent_code = data["continent_code"] or "Unknown"
        in_eu = data["in_eu"]
        postal = data["postal"] or "Unknown"
        latitude = data["latitude"] or "Unknown"
        longitude = data["longitude"] or "Unknown"
        country_timezone = data["timezone"] or "Unknown"
        utc_offset = data["utc_offset"] or "Unknown"
        dial_code = data["country_calling_code"] or "Unknown"
        currency = data["currency"] or "Unknown"
        languages = data["languages"] or "Unknown"
        organization = data["org"] or "Unknown"
        asn = data["asn"] or "Unknown"
        
        embd = hikari.Embed(
            title="IP Information", color=ctx.author.accent_colour, timestamp=datetime.datetime.now().astimezone())
        embd.add_field(name="IP Address:", value=ipaddr, inline=False)
        embd.add_field(name="ISP Name/Organization:",value=organization, inline=False)
        embd.add_field(name="City:", value=city, inline=False)
        embd.add_field(name="Regional Area:", value=region)
        embd.add_field(name="Region Code:",value=region_code, inline=False)
        embd.add_field(name="Postal Code:", value=postal, inline=False)
        embd.add_field(name="Country:", value=country, inline=False)
        embd.add_field(name="Country Name:",value=country_name, inline=False)
        embd.add_field(name="Country Code (ISO):",value=country_code_iso3, inline=False)
        embd.add_field(name="Language Spoken:",value=languages, inline=False)
        embd.add_field(name="Continent Code:",value=continent_code, inline=False)
        embd.add_field(name="Is country a member of European Union (EU)?", value=in_eu, inline=False)
        embd.add_field(name="Latitude Coordinate:",value=latitude, inline=False)
        embd.add_field(name="Longitude Coordinate:",value=longitude, inline=False)
        embd.add_field(name="Timezone:",value=country_timezone, inline=False)
        embd.add_field(name="UTC Offset:", value=utc_offset, inline=False)
        embd.add_field(name="Country Dial Code:",value=dial_code, inline=False)
        embd.add_field(name="Currency:", value=currency, inline=False)
        embd.add_field(name="Autonomous System Number:",value=asn, inline=False)
        await ctx.respond(embed=embd)
    else:
        raise ValueError("⚠ An Error Occured! Make sure the IP and the formatting are correct!")

def load(bot):
    bot.add_plugin(ip_plugin)

def unload(bot):
    bot.remove_plugin(ip_plugin)
