from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from AviaxMusic import app
from config import SUPPORT_CHAT

# ✅ Help Texts
HELP_1 = """<b><u>Admin Commands:</u></b>

/pause - Pause the current stream.
/resume - Resume the paused stream.
/skip - Skip to the next track.
/stop - Stop playback and clear the queue.
/player - Get the interactive player panel.
/queue - Show the queued tracks.
"""

HELP_2 = """
<b><u>Auth Users:</u></b>

Auth users can use admin commands without admin rights.
/auth [username or user_id]
/unauth [username or user_id]
/authusers - Show all auth users.
"""

HELP_3 = """
<b><u>Broadcast (Only Sudo):</u></b>
/broadcast [message or reply to a message]
Options:
-pin, -pinloud, -user, -assistant
Example:
/broadcast -user -assistant -pin Testing broadcast
"""

HELP_MAIN = """
<b>✅ Help Menu</b>

Select a category below:
"""

# ✅ Help Keyboard
HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Admin", callback_data="help_admin"),
         InlineKeyboardButton("Auth", callback_data="help_auth")],
        [InlineKeyboardButton("Broadcast", callback_data="help_broadcast")],
        [InlineKeyboardButton("Support", url=SUPPORT_CHAT)]
    ]
)

# ✅ Main Help Command
@app.on_message(filters.command("help") & ~filters.private)
async def help_command(_, message):
    await message.reply_text(
        HELP_MAIN,
        reply_markup=HELP_BUTTONS
    )

# ✅ Callback Queries for Help Menu
@app.on_callback_query(filters.regex("^help_"))
async def help_callback(_, query):
    data = query.data.split("_")[1]

    if data == "admin":
        text = HELP_1
    elif data == "auth":
        text = HELP_2
    elif data == "broadcast":
        text = HELP_3
    else:
        text = HELP_MAIN

    await query.message.edit_text(text, reply_markup=HELP_BUTTONS)
