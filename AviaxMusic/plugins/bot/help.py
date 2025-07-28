from pyrogram import filters
from pyrogram.types import Message
from AviaxMusic import app
from AviaxMusic.misc import SUDOERS
from AviaxMusic.utils.decorators.language import language
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ✅ HELP command list
HELP_COMMAND = ["help", "commands"]

# ✅ All HELP text (already given by you)
HELP_1 = """<b><u>ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

ᴊᴜsᴛ ᴀᴅᴅ <b>ᴄ</b> ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.

/pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.
/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
/end or /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ.
/player : ɢᴇᴛ ᴀ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ.
/queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇ ʟɪsᴛ.
"""

HELP_2 = """
<b><u>ᴀᴜᴛʜ ᴜsᴇʀs :</b></u>

ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ʙᴏᴛ.

/auth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ]
/unauth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ]
/authusers
"""

HELP_3 = """
<u><b>ʙʀᴏᴀᴅᴄᴀsᴛ :</b></u>
/broadcast [message or reply] : ʙʀᴏᴀᴅᴄᴀsᴛ to all served chats.
"""

HELP_4 = """
<u><b>ᴄʜᴀᴛ ʙʟᴀᴄᴋʟɪsᴛ :</b></u>
/blacklistchat [chat id]
/whitelistchat [chat id]
/blacklistedchat
"""

HELP_5 = """
<u><b>ʙʟᴏᴄᴋ ᴜsᴇʀs:</b></u>
/block [username or reply]
/unblock [username or reply]
/blockedusers
"""

HELP_6 = """
<u><b>ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ :</b></u>
/cplay [track name]
/cvplay [video name]
/channelplay [username or id]
"""

HELP_7 = """
<u><b>ɢʟᴏʙᴀʟ ʙᴀɴ :</b></u>
/gban [username or reply]
/ungban [username or reply]
/gbannedusers
"""

HELP_8 = """
<u><b>ʟᴏᴏᴘ :</b></u>
/loop [enable/disable]
/loop [1, 2, 3...]
"""

HELP_9 = """
<u><b>ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ :</b></u>
/logs
/logger [enable/disable]
/maintenance [enable/disable]
"""

HELP_10 = """
<b><u>ᴘɪɴɢ & sᴛᴀᴛs :</b></u>
/start
/help
/ping
/stats
"""

HELP_11 = """
<u><b>ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs :</b></u>
/play or /vplay
/playforce or /vplayforce
"""

HELP_12 = """
<b><u>sʜᴜғғʟᴇ ᴏ̨ᴜᴇᴜᴇ :</b></u>
/shuffle
/queue
"""

HELP_13 = """
<b><u>sᴇᴇᴋ :</b></u>
/seek [seconds]
/seekback [seconds]
"""

HELP_14 = """
<b><u>sᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅ :</b></u>
/song [song name or link]
"""

HELP_15 = """
<b><u>sᴘᴇᴇᴅ :</b></u>
/speed or /playback
/cspeed or /cplayback
"""

HELP_16 = """
<b><u>ᴘʀɪᴠᴀᴄʏ :</b></u>
/privacy
"""

HELP_TEXTS = [
    HELP_1, HELP_2, HELP_3, HELP_4, HELP_5,
    HELP_6, HELP_7, HELP_8, HELP_9, HELP_10,
    HELP_11, HELP_12, HELP_13, HELP_14, HELP_15, HELP_16
]

# ✅ Command
@app.on_message(filters.command(HELP_COMMAND) & ~filters.edited)
@language
async def help_command(client, message: Message, _):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("CLOSE", callback_data="close")]]
    )
    text = "\n\n".join(HELP_TEXTS)
    await message.reply_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
