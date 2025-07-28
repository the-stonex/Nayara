from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from AviaxMusic import app
from AviaxMusic.utils.inline.start import private_panel
from config import START_IMG_URL, SUPPORT_CHAT
from strings import get_string
from AviaxMusic.utils.database import get_lang


@app.on_message(filters.command("start") & filters.private)
async def start_pm(client, message: Message):
    language = await get_lang(message.chat.id)
    _ = get_string(language)

    keyboard = InlineKeyboardMarkup(private_panel(_))

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["start_2"].format(app.mention),
        reply_markup=keyboard
    )


@app.on_message(filters.command("start") & filters.group)
async def start_gp(client, message: Message):
    language = await get_lang(message.chat.id)
    _ = get_string(language)

    text = _["start_1"].format(app.mention)
    button = [[InlineKeyboardButton("Support", url=SUPPORT_CHAT)]]

    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(button))
