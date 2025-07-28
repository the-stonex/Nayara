from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AviaxMusic import app
from AviaxMusic.misc import SUDOERS
from AviaxMusic.utils.decorators import language, languageCB
from strings import get_command
from config import SUPPORT_CHAT

HELP_COMMAND = get_command("HELP_COMMAND")


@app.on_message(filters.command(HELP_COMMAND) & filters.group & ~filters.edited)
@language
async def help_command(_, message, language):
    buttons = [
        [
            InlineKeyboardButton(text="📚 Admin Commands", callback_data="help_admin"),
            InlineKeyboardButton(text="🎧 Play Commands", callback_data="help_play"),
        ],
        [
            InlineKeyboardButton(text="🔒 Privacy", callback_data="help_privacy"),
            InlineKeyboardButton(text="📨 Support", url=SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text="❌ Close", callback_data="close"),
        ]
    ]
    await message.reply_text(
        text=language["help_1"],  # Default text for help intro
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("help_(.*)"))
@languageCB
async def help_callback(_, CallbackQuery, language):
    query = CallbackQuery.data.split("_")[1]
    
    if query == "admin":
        text = language["help_admin"]
    elif query == "play":
        text = language["help_play"]
    elif query == "privacy":
        text = language["help_privacy"]
    else:
        text = language["help_1"]

    buttons = [
        [
            InlineKeyboardButton(text="⬅ Back", callback_data="help_back"),
            InlineKeyboardButton(text="❌ Close", callback_data="close"),
        ]
    ]
    await CallbackQuery.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("help_back"))
@languageCB
async def help_back(_, CallbackQuery, language):
    buttons = [
        [
            InlineKeyboardButton(text="📚 Admin Commands", callback_data="help_admin"),
            InlineKeyboardButton(text="🎧 Play Commands", callback_data="help_play"),
        ],
        [
            InlineKeyboardButton(text="🔒 Privacy", callback_data="help_privacy"),
            InlineKeyboardButton(text="📨 Support", url=SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text="❌ Close", callback_data="close"),
        ]
    ]
    await CallbackQuery.message.edit_text(
        text=language["help_1"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )
