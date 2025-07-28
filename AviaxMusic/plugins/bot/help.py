from pyrogram import filters
from pyrogram.types import Message
from AviaxMusic import app
from AviaxMusic.misc import SUDOERS
from strings import get_command
from AviaxMusic.utils.decorators.language import language

# Command names
HELP_COMMAND = get_command("HELP_COMMAND")

# Help texts
HELP_1 = """<b><u>ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

ᴊᴜsᴛ ᴀᴅᴅ <b>ᴄ</b> ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.
...
"""

HELP_2 = """
<b><u>ᴀᴜᴛʜ ᴜsᴇʀs :</b></u>
...
"""

HELP_3 = """
<u><b>ʙʀᴏᴀᴅᴄᴀsᴛ ғᴇᴀᴛᴜʀᴇ</b></u>
...
"""

# Add all HELP_x like above (1 to 16) exactly as before

# Combine help pages in a dict for easy navigation
HELP_PAGES = {
    "admin": HELP_1,
    "auth": HELP_2,
    "broadcast": HELP_3,
    # ... Add all keys for HELP_4, HELP_5 etc
}

@app.on_message(filters.command(HELP_COMMAND) & filters.group)
@language
async def help_command(client, message: Message, _):
    text = "<b>❓ Help Menu</b>\n\nSelect a category:\n\n"
    for key in HELP_PAGES.keys():
        text += f"• <code>{key}</code>\n"
    text += "\nUse `/help [category]` to view details."
    await message.reply_text(text)

@app.on_message(filters.command(HELP_COMMAND) & filters.group)
async def help_category(client, message: Message):
    if len(message.command) == 1:
        return
    category = message.command[1].lower()
    if category in HELP_PAGES:
        await message.reply_text(HELP_PAGES[category])
    else:
        await message.reply_text("❌ Invalid category. Use `/help` to see available categories.")
