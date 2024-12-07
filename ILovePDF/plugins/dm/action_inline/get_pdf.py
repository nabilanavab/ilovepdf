# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/action_inline/get_pdf.py"


from . import *
from pyrogram.types import InputMediaDocument


async def download(current, total, bot, callbackQuery):
    try:
        await bot.edit_inline_reply_markup(
            inline_message_id=callbackQuery.inline_message_id,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "📥 DOWNLOADED {:.2f}% 📥".format(current / total * 100),
                        callback_data=f"{callbackQuery.data}",)
                ],[
                    InlineKeyboardButton(
                        "🗑️ CANCEL 🗑️", callback_data=f"c{callbackQuery.data[1:]}")
                ]]
            )
        )
    except errors.MessageNotModified as e:
        logger.debug("🐞 %s: %s" % (file_name, e))
    except errors.FloodWait as e:
        logger.debug("🐞 %s: %s" % (file_name, e))
        await asyncio.sleep(e.x)
    except Exception as e:
        logger.debug("🐞 %s: %s" % (file_name, e))


@ILovePDF.on_callback_query(filters.regex("lib"))
async def pdfDriver(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.from_user.id)
        trCHUNK, _ = await translate(text="INLINE", lang_code=lang_code)

        if not (callbackQuery.from_user.id == int(callbackQuery.data.split("|")[2])):
            return await callbackQuery.answer(trCHUNK["cbNotU"])

        getMSG = await bot.get_messages(
            chat_id=int(log.LOG_CHANNEL),
            message_ids=int(callbackQuery.data.split("|")[1]),
        )

        if getMSG.empty:
            return await callbackQuery.answer(trCHUNK["old"])

        if await work(callbackQuery, "check", False):
            return await callbackQuery.answer(trCHUNK["inWork"])
        cDIR = await work(callbackQuery, "create", False)

        await bot.edit_inline_reply_markup(
            inline_message_id=callbackQuery.inline_message_id,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                       "🍪 COOKING DATA 🍪", callback_data=f"{callbackQuery.data}"
                    )
                ],[
                    InlineKeyboardButton(
                        "🗑️ CANCEL 🗑️", callback_data=f"c{callbackQuery.data[1:]}")
                ]]
            ),
        )

        caption = getMSG.caption
        md5 = caption.splitlines()[0].split(":")[1].strip()
        link = f"http://library.lol/main/{md5}"

        file = await Libgen().download(
            link,
            dest_folder=cDIR,
            progress=download,
            progress_args=[bot, callbackQuery],
        )

        await bot.edit_inline_reply_markup(
            inline_message_id=callbackQuery.inline_message_id,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "🐍 STARTED UPLOADING 🐍", callback_data=f"{callbackQuery.data}",)
                ],[
                    InlineKeyboardButton(
                        "🗑️ CANCEL 🗑️", callback_data=f"c{callbackQuery.data[1:]}")
                ]]
            ),
        )

        await bot.edit_inline_media(
            inline_message_id=callbackQuery.inline_message_id,
            media=InputMediaDocument(media=file, caption=getMSG.caption),
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        text="♻️ SEARCH AGAIN ♻️", switch_inline_query_current_chat="",)
                ]]
            ),
        )
        return await work(callbackQuery, "delete", False)

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        await work(callbackQuery, "delete", False)


@ILovePDF.on_callback_query(filters.regex("^cD\|"))
async def close(bot, callbackQuery):
    try:
        if not (callbackQuery.from_user.id == int(callbackQuery.data.split("|")[2])):
            return await callbackQuery.answer("message not for you..")

        await callbackQuery.answer("🗑️")
        await work(callbackQuery, "delete", False)
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=False)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
