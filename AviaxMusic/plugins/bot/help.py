from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from AviaxMusic import app
from strings import get_string
from config import SUPPORT_GROUP

# ✅ Help Text Sections
HELP_SECTIONS = {
    "start": """
<b>Help Menu</b>
Select a category below to view commands:
""",
    "admin": """<b>Admin Commands:</b>
/pause - Pause the stream
/resume - Resume the stream
/skip - Skip the current stream
/stop - End streaming
/player - Show player panel
/queue - Show queue
""",
    "auth": """<b>Auth Users:</b>
/auth [user_id] - Add user as auth
/unauth [user_id] - Remove auth user
/authusers - Show auth users list
""",
    "play": """<b>Play Commands:</b>
/play [song name] - Play audio
/vplay [video name] - Play video
/forceplay - Force play a track
""",
    "gban": """<b>Global Ban:</b>
/gban [user_id] - Ban globally
/ungban [user_id] - Unban globally
/gbannedusers - Show GBan list
""",
    "broadcast": """<b>Broadcast:</b>
/broadcast [message] - Broadcast to all chats
Options: -pin, -user, -assistant
""",
    "maintenance": """<b>Maintenance:</b>
/maintenance [enable|disable] - Enable/Disable maintenance
/logs - Get logs
""",
    "speed": """<b>Speed Control:</b>
/speed - Change playback speed
/cspeed - Change channel speed
""",
    "loop": """<b>Loop Streaming:</b>
/loop [1,2,3...] - Enable loop for track
/loop disable - Disable loop
""",
    "privacy": """<b>Privacy:</b>
/privacy - Show bot privacy policy
"""
}

# ✅ Main Menu Buttons
def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎛 Admin", callback_data="help_admin"),
         InlineKeyboardButton("👤 Auth", callback_data="help_auth")],
        [InlineKeyboardButton("🎵 Play", callback_data="help_play"),
         InlineKeyboardButton("🔐 Privacy", callback_data="help_privacy")],
        [InlineKeyboardButton("📢 Support", url=SUPPORT_GROUP),
         InlineKeyboardButton("❌ Close", callback_data="close")]
    ])

# ✅ Command Handler
@app.on_message(filters.command(["help"]))
async def help_menu(client, message):
    await message.reply_text(
        HELP_SECTIONS["start"],
        reply_markup=main_buttons()
    )

# ✅ Callback Handler
@app.on_callback_query(filters.regex("^help_"))
async def help_callback(client, query: CallbackQuery):
    section = query.data.replace("help_", "")
    text = HELP_SECTIONS.get(section, "Invalid Section!")
    await query.message.edit_text(
        text,
        reply_markup=main_buttons()
    )

# ✅ Close Button
@app.on_callback_query(filters.regex("^close$"))
async def close_button(client, query: CallbackQuery):
    await query.message.delete()
