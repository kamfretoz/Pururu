import hikari
import lightbulb

morseAlphabet = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    " ": "/",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    "?": "..--..",
    "'": ".----.",
    "-": "-....-",
    "/": "-..-.",
    "@": ".--.-.",
    "=": "-...-"
}

morse_plugin = lightbulb.Plugin("morse", "BEEP BEEP")

@morse_plugin.command()
@lightbulb.command("morse", "Allows you to encode or decode morse codes")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def morse(ctx: lightbulb.Context) -> None:
    pass

@morse.child()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("input", "the morse code you want to decode", type = str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("decode", "to decode the morse code")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def morse_decode(ctx: lightbulb.Context) -> None:
        text = ctx.options.input

        inverseMorseAlphabet = dict((v, k) for (k, v) in morseAlphabet.items())

        messageSeparated = text.split(' ')
        decodeMessage = ''
        for char in messageSeparated:
            if char in inverseMorseAlphabet:
                decodeMessage += inverseMorseAlphabet[char]
            else:
                decodeMessage += '<ERROR>'
                
        await ctx.respond(embed=hikari.Embed(title="Morse to ASCII Conversion:", description=decodeMessage))

@morse.child()
@lightbulb.add_cooldown(3, 3, lightbulb.cooldowns.UserBucket)
@lightbulb.option("input", "the text you want to encode", type = str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command("encode", "to encode the ASCII text")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def morse_encode(ctx: lightbulb.Context) -> None:
    
        text = ctx.options.input
    
        encodedMessage = ""
        for char in text[:]:
            if char.upper() in morseAlphabet:
                encodedMessage += morseAlphabet[char.upper()] + " "
            else:
                encodedMessage += '<???>'
                
        await ctx.respond(embed=hikari.Embed(title="ASCII to Morse Conversion:", description=encodedMessage))
        
def load(bot) -> None:
    bot.add_plugin(morse_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(morse_plugin)
