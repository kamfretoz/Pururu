
import os
from hikari import Intents
import dotenv

dotenv.load_dotenv()

#
# MAIN BOT RELATED
#

INTENTS = (
    Intents.GUILDS               |
    Intents.GUILD_VOICE_STATES   |
    Intents.GUILD_MESSAGES       |
    Intents.MESSAGE_CONTENT
)

GUILDS = (
    393724666474135552,
    535677066138353674,
    617173140476395542,
    793239269723471902,
    875986914367385600
)

TOKEN=os.getenv("BOT_TOKEN")
PREFIX = os.environ["PREFIX"]


#
# MUSIC RELATED
#

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
SPOTCLIENT_ID=os.getenv("SPOTID")
SPOTCLIENT_SECRET=os.getenv("SPOTSECRET")
LAVALINK_SERVER=os.getenv("LAVA_SRV")
LAVALINK_PORT=os.getenv("LAVA_PORT")
LAVALINK_PASSWORD=os.getenv("LAVA_PASS")
LAVALINK_SSL=os.getenv("LAVA_SSL")