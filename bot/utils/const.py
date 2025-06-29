import os
import dotenv
from hikari import Intents
from hikari.impl.config import CacheSettings
from hikari.api.config import CacheComponents

#
# MAIN BOT RELATED
#

GUILDS = [
        875986914367385600,
        570976409452019722
]

CACHE = CacheSettings(components=
        CacheComponents.ALL
)
