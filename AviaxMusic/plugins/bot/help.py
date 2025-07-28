from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AviaxMusic import app
from strings import HELP_1, HELP_2, HELP_3, HELP_4, HELP_5, HELP_6, HELP_7, HELP_8, HELP_9, HELP_10, HELP_11, HELP_12, HELP_13, HELP_14, HELP_15, HELP_16

HELP_COMMAND = ["help", "commands"]

# ✅ FloodWait handling
from pyrogram.errors import FloodWait
import asyncio

# ✅ Remove filters.edited (old version issue)
@app.on_message(filters.command(HELP_COMMAND))
async def help_command(client, message):
    try:
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Admin Commands", callback_data="help_1")],
                [InlineKeyboardButton("Auth Users", callback_data="help_2")],
                [InlineKeyboardButton("Broadcast", callback_data="help_3")],
                [InlineKeyboardButton("Close", callback_data="close")]
            ]
        )
        await message.reply_text(
            "✅ Here is the help menu. Choose an option below:",
            reply_markup=keyboard
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)

# ✅ Callback query handling
@app.on_callback_query(filters.regex("help_"))
async def help_callback(client, query):
    section = query.data.split("_")[1]

    text = ""
    if section == "1":
        text = HELP_1
    elif section == "2":
        text = HELP_2
    elif section == "3":
        text = HELP_3
    elif section == "4":
        text = HELP_4
    elif section == "5":
        text = HELP_5
    elif section == "6":
        text = HELP_6
    elif section == "7":
        text = HELP_7
    elif section == "8":
        text = HELP_8
    elif section == "9":
        text = HELP_9
    elif section == "10":
        text = HELP_10
    elif section == "11":
        text = HELP_11
    elif section == "12":
        text = HELP_12
    elif section == "13":
        text = HELP_13
    elif section == "14":
        text = HELP_14
    elif section == "15":
        text = HELP_15
    elif section == "16":
        text = HELP_16

    await query.message.edit_text(text)
