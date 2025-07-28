from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from pyrogram.enums import ParseMode

from AviaxMusic import app
from AviaxMusic.utils import help_pannel
from AviaxMusic.utils.database import get_lang
from AviaxMusic.utils.decorators.language import LanguageStart, languageCB
from AviaxMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string
from AviaxMusic.misc import SUDOERS
from AviaxMusic.utils.stuffs.helper import Helper  # अगर ये मौजूद नहीं है तो हटा देना

# ✅ Fallback if SUPPORT_CHAT is empty
if not SUPPORT_CHAT:
    SUPPORT_CHAT = "https://t.me/YourSupportGroup"

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("abot_cb") & ~BANNED_USERS)
async def abot_callback(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_B,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="settings_back_helper")]]
        ),
    )


@app.on_callback_query(filters.regex("ubot_cb") & ~BANNED_USERS)
async def ubot_callback(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_B,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="settings_back_helper")]]
        ),
    )
