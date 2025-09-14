import os
import re
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env (for local development)
load_dotenv()

# ✅ Telegram API credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Database
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

# ✅ Duration limit in minutes
DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT", 999999))

# ✅ IDs
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", 0))
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# ✅ Heroku
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

# ✅ External API for music
API_URL = getenv("API_URL", 'https://api.thequickearn.xyz') #youtube song url
VIDEO_API_URL = getenv("VIDEO_API_URL", 'https://api.video.thequickearn.xyz')
API_KEY = getenv("API_KEY", None) # youtube song api key, generate free key or buy paid plan from panel.thequickearn.xyz

# ✅ Repo details
UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/the-stonex/Nayara")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = os.getenv("GIT_TOKEN")

# ✅ Support links
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/+YTsbDmCAJxVkMTc1")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/+uzSTnYDHsVo2NzJl")
SUPPORT_GROUP = SUPPORT_CHAT  # Compatibility for old code

# ✅ Privacy Policy
PRIVACY_LINK = os.getenv("PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-AviaxMusic-08-14")

# ✅ Auto-leaving setting
AUTO_LEAVING_ASSISTANT = os.getenv("AUTO_LEAVING_ASSISTANT", "True").lower() in ["true", "1", "yes"]

# ✅ Spotify
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# ✅ Playlist limit
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", 25))

# ✅ File size limits
TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))  # 100 MB
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))  # 2 GB

# ✅ Pyrogram session strings
STRING1 = os.getenv("STRING_SESSION")
STRING2 = os.getenv("STRING_SESSION2")
STRING3 = os.getenv("STRING_SESSION3")
STRING4 = os.getenv("STRING_SESSION4")
STRING5 = os.getenv("STRING_SESSION5")

# ✅ Filters and dicts
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ✅ Image URLs
START_IMG_URL = os.getenv("START_IMG_URL", "https://files.catbox.moe/y030tk.mp4")
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://graph.org//file/389a372e8ae039320ca6c.png")
PLAYLIST_IMG_URL = "https://graph.org//file/3dfcffd0c218ead96b102.png"
STATS_IMG_URL = "https://files.catbox.moe/4pnek9.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
TELEGRAM_VIDEO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
STREAM_IMG_URL = "https://te.legra.ph/file/bd995b032b6bd263e2cc9.jpg"
SOUNCLOUD_IMG_URL = "https://te.legra.ph/file/bb0ff85f2dd44070ea519.jpg"
YOUTUBE_IMG_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"

# ✅ Convert time to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# ✅ URL Validation
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL URL must start with https://")

if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - SUPPORT_CHAT URL must start with https://")

