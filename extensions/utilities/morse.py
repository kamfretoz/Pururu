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

def encode(value: str):
    encodedMessage = ""
    for char in value[:]:
        if char.upper() in morseAlphabet:
            encodedMessage += morseAlphabet[char.upper()] + " "
        else:
            encodedMessage += '<???>'
    return encodedMessage

def decode(value: str):
    inverseMorseAlphabet = dict((v, k) for (k, v) in morseAlphabet.items())
    messageSeparated = value.split(' ')
    decodedMessage = ''
    for char in messageSeparated:
        if char in inverseMorseAlphabet:
            decodedMessage += inverseMorseAlphabet[char]
        else:
            decodedMessage += '<ERROR>'
    return decodedMessage

@morse_plugin.command
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("input", "the text you want to encode", str, required = True, modifier = lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("mode", "the conversion mode", str, required = True, choices=["encode", "decode"])
@lightbulb.command("morse", "to encode or decode morse code", pass_options = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def morse(ctx: lightbulb.Context, mode:str, input: str) -> None:
    if mode == "encode":
        direction = "ASCII 🡪 Morse"
        result = encode(input)
    elif mode == "decode":
        direction = "ASCII 🡨 Morse"
        result = decode(input)
    else:
        await ctx.respond("Invalid Mode Entered.")
        return
            
    await ctx.respond(embed=hikari.Embed(title=f"{direction} Conversion:", description=result))
        
def load(bot) -> None:
    bot.add_plugin(morse_plugin)
    
def unload(bot) -> None:
    bot.remove_plugin(morse_plugin)
