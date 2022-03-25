
import os
import dotenv
import lightbulb

dotenv.load_dotenv()

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
SPOTCLIENT_ID=os.getenv("SPOTID")
SPOTCLIENT_SECRET=os.getenv("SPOTSECRET")
TOKEN=os.getenv("BOT_TOKEN")
LAVALINK_SERVER=os.getenv("LAVA_SRV")
LAVALINK_PORT=os.getenv("LAVA_PORT")
LAVALINK_PASSWORD=os.getenv("LAVA_PASS")
LAVALINK_SSL=os.getenv("LAVA_SSL")