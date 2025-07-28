from typing import Union
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from AviaxMusic import app
from AviaxMusic.utils import help_pannel
from AviaxMusic.utils.database import get_lang
from AviaxMusic.utils.decorators.language import LanguageStart, languageCB
from AviaxMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT  # ✅ SUPPORT_GROUP → SUPPORT_CHAT (fix)
from strings import get_string, helpers

# ✅ PRIVATE HELP COMMAND OR CALLBACK
@app.on_message(filters.command("help") & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: Client, update: Union[types.Message, types.CallbackQuery]):
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
            _["help_1"].format(SUPPORT_CHAT),  # ✅ SUPPORT_GROUP → SUPPORT_CHAT
            reply_markup=keyboard
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
            caption=_["help_1"].format(SUPPORT_CHAT),  # ✅ SUPPORT_GROUP → SUPPORT_CHAT
            reply_markup=keyboard
        )

# ✅ GROUP HELP COMMAND
@app.on_message(filters.command("help") & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client: Client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ✅ CALLBACK HANDLER FOR HELP BUTTONS
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client: Client, CallbackQuery, _):
    try:
        cb = CallbackQuery.data.strip().split(None, 1)[1]
    except IndexError:
        cb = None

    keyboard = help_back_markup(_)
    if cb == "hb16":
        text = helpers.HELP_16.format(app.name)
    else:
        text = getattr(helpers, f"HELP_{cb[2:]}", "No help available.")

    await CallbackQuery.edit_message_text(
        text,
        reply_markup=keyboard
    )
