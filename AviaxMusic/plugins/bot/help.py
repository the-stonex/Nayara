from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT_CHAT

HELP_1 = """<b><u>ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

ᴊᴜsᴛ ᴀᴅᴅ <b>ᴄ</b> ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.

...
"""

@app.on_message(filters.command("help"))
async def help_command(client, message):
    buttons = [
        [InlineKeyboardButton("Support Chat", url=SUPPORT_CHAT)],
        [InlineKeyboardButton("Close", callback_data="close")]
    ]
    await message.reply_text(
        text="Help Menu",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
