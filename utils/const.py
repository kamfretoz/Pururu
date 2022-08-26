
import os
import dotenv
from hikari import Intents
from hikari.impl.config import CacheSettings
from hikari.api.config import CacheComponents

dotenv.load_dotenv()

#
# MAIN BOT RELATED
#

GUILDS = (
        875986914367385600,
        617173140476395542,
        793239269723471902,
        535677066138353674,
        570976409452019722
)

PREFIX = [
        "x!",
        "X!"
        ]

INTENTS = (
        Intents.GUILDS                      |
        Intents.GUILD_MEMBERS               |
        Intents.GUILD_MESSAGES              |
        Intents.GUILD_VOICE_STATES          |
        Intents.MESSAGE_CONTENT             
)


CACHE = CacheSettings(components=
        CacheComponents.GUILDS              |
        CacheComponents.GUILD_CHANNELS      |
        CacheComponents.ME                  |
        CacheComponents.MEMBERS             |
        CacheComponents.MESSAGES            |
        CacheComponents.ROLES               |
        CacheComponents.VOICE_STATES    
)

TOKEN = os.getenv("BOT_TOKEN")


#
# MUSIC RELATED
#

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
SPOTCLIENT_ID = os.getenv("SPOTID")
SPOTCLIENT_SECRET = os.getenv("SPOTSECRET")
LAVALINK_SERVER = os.getenv("LAVA_SRV")
LAVALINK_PORT = os.getenv("LAVA_PORT")
LAVALINK_PASSWORD = os.getenv("LAVA_PASS")