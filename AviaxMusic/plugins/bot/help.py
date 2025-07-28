from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode

from AviaxMusic import app
from AviaxMusic.utils import help_pannel
from AviaxMusic.utils.database import get_lang
from AviaxMusic.utils.decorators.language import LanguageStart
from AviaxMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL
from strings import get_string
from AviaxMusic.misc import SUDOERS
from AviaxMusic.utils.stuffs.buttons import BUTTONS
from AviaxMusic.utils.stuffs.helper import Helper

# ✅ Support Group Link
SUPPORT_CHAT = "https://t.me/YourSupportGroup"  # Change this to your group link


# ✅ HELP Command in Private
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


# ✅ HELP Command in Groups
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


# ✅ About Callback Button
@app.on_callback_query(filters.regex("abot_cb") & ~BANNED_USERS)
async def abot_callback(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_B,
        reply_markup=InlineKeyboardMarkup(BUTTONS.ABUTTON)
    )


# ✅ Ubot Callback Button
@app.on_callback_query(filters.regex("ubot_cb") & ~BANNED_USERS)
async def ubot_callback(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_B,
        reply_markup=InlineKeyboardMarkup(BUTTONS.UBUTTON)
    )
