# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/refresh.py"

from plugins import *
from ..photo import images
from plugins.utils import *
from configs.db import myID
from ..document import documents
from configs.db import invite_link
from configs.config import settings
from .file_process.link import decode
from plugins.group.document import gDOC
from ..action_inline.in_bot import openInBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@ILovePDF.on_callback_query(filters.regex("^refresh"))
async def _refresh(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return

        if invite_link:
            try:
                userStatus = await bot.get_chat_member(
                    str(settings.UPDATE_CHANNEL), callbackQuery.from_user.id
                )
                if userStatus.status == "kicked":
                    return await callbackQuery.answer("🤧")
            except Exception:
                tTXT, _ = await util.translate(text="BAN['Fool']", lang_code=lang_code)
                return await callbackQuery.answer(tTXT, show_alert=True)

        if callbackQuery.data.startswith("refresh-g"):  # this means "refresh-g{code}
            await decode(
                bot, callbackQuery.data[9:], callbackQuery.message, lang_code, cb=True
            )
            return await callbackQuery.message.delete()

        elif callbackQuery.data.startswith("refresh-m"):  # this means "refresh-g{code}
            await openInBot(bot, callbackQuery.message, callbackQuery.data.split("-m"))
            return await callbackQuery.message.delete()

        elif await work.work(callbackQuery, "check", False):
            tTXT, _ = await util.translate(
                text="PROGRESS['workInP']", lang_code=lang_code
            )
            return await callbackQuery.answer(tTXT)

        elif callbackQuery.message.reply_to_message.document:
            await callbackQuery.message.delete()
            return await documents(bot, callbackQuery.message.reply_to_message)

        elif callbackQuery.message.reply_to_message.photo:
            await callbackQuery.message.delete()
            return await images(bot, callbackQuery.message.reply_to_message)

        elif callbackQuery.message.reply_to_message.text.startswith("/start"):
            tTXT, tBTN = await util.translate(
                text="HOME['HomeA']",
                button="HOME['HomeACB']",
                lang_code=lang_code,
                order=2121,
            )
            await callbackQuery.edit_message_caption(
                caption=tTXT.format(callbackQuery.from_user.mention, myID[0].mention),
                reply_markup=tBTN,
            )
            tTXT, tBTN = await util.translate(
                text="HOME['search']", lang_code=lang_code
            )
            await callbackQuery.message.reply_sticker(
                sticker="CAACAgIAAxkBAAEVZ65kduZn7WTQXlyDFErYqb0BvyoIEQACVQADr8ZRGmTn_PAl6RC_LwQ",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=tTXT[0], switch_inline_query_current_chat=""
                            )
                        ],
                        [InlineKeyboardButton(text=tTXT[1], callback_data="beta")],
                    ]
                ),
            )
            return await callbackQuery.message.reply_to_message.delete()

        elif callbackQuery.message.reply_to_message.text.startswith("/"):
            await callbackQuery.message.delete()
            return await gDOC(bot, callbackQuery.message.reply_to_message)

        elif callbackQuery.message.reply_to_message.text:
            await callbackQuery.message.delete()
            return await _url(bot, callbackQuery.message.reply_to_message)

    except Exception as Error:
        logger.debug(f"{file_name}: {Error}")

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
