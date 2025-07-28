from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton

from AviaxMusic import app
from AviaxMusic.utils import help_pannel
from AviaxMusic.utils.database import get_lang
from AviaxMusic.utils.decorators.language import LanguageStart, languageCB
from AviaxMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers
from AviaxMusic.misc import SUDOERS


# ✅ Private Help Command
@app.on_message(filters.command("help") & filters.private & ~BANNED_USERS)
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


# ✅ Group Help Command
@app.on_message(filters.command("help") & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


# ✅ Help Callback Buttons
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    if cb == "hb6" and CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer("You are not a sudo user.", show_alert=True)

    help_text = getattr(helpers, f"HELP_{cb[2:]}", None)
    if help_text:
        await CallbackQuery.edit_message_text(help_text, reply_markup=keyboard)
    else:
        await CallbackQuery.answer("Invalid Option!", show_alert=True)


# ✅ Extra Callback Buttons for Advanced Panel
@app.on_callback_query(filters.regex("extra_help") & ~BANNED_USERS)
async def extra_help(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        "Advanced Help Menu:\n\nUse buttons below to explore features.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("↺ Back", callback_data="settings_back_helper")],
            ]
        ),
    )
