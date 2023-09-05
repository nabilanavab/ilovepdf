# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/utils/render.py"

import fitz
from .util import *
from plugins import *
from .work import work
from logger import logger
from pyrogram.types import Message
from pyrogram import Client, filters
from configs.config import dm, settings
from pyrogram.enums import ChatMemberStatus, ChatType, ChatAction

# CHECKS CALLBACKQUERY USER 
async def header(
    bot, callbackQuery, lang_code: str=settings.DEFAULT_LANG, doc: bool=True
):
    """
    This function is designed to check if a certain process needs to be executed [only for callbackQuery],
    particularly in groups where callback messages from different users can cause confusion and unwanted errors for the bot.
    """
    try:
        if not doc:
            if (
                callbackQuery.message.chat.type != ChatType.PRIVATE
                and callbackQuery.from_user.id not in dm.ADMINS
            ):
                userStat = await bot.get_chat_member(
                    callbackQuery.message.chat.id, callbackQuery.from_user.id
                )
                if userStat.status not in [
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.OWNER,
                ]:
                    _, __ = await translate(text="BAN['cbNotU']", lang_code=lang_code)
                    await callbackQuery.answer(_, show_alert=True)
                    return True
            return False

        # Trying to fetch the callbackQuery.message.reply_to_message from a callbackQuery can result in an error
        # if the original message has been deleted. This can happen if the user deletes the PDF after it has been sent,
        # which can result in the message being deleted and the callbackQuery referencing a non-existent message, causing an error.
        fileExist = callbackQuery.message.reply_to_message

        # "If the callback query is from a private message (PM), the code will be executed.
        # Otherwise, it checks whether the sender of the PDF and callback are the same,
        # or if they are in a group and the bot admin, before executing the code."
        if (
            callbackQuery.message.chat.type != ChatType.PRIVATE
            and callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id
            and callbackQuery.from_user.id not in dm.ADMINS
        ):
            userStat = await bot.get_chat_member(
                callbackQuery.message.chat.id, callbackQuery.from_user.id
            )
            if userStat.status not in [
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            ]:
                _, __ = await translate(text="BAN['cbNotU']", lang_code=lang_code)
                await callbackQuery.answer(_, show_alert=True)
                return True
        return False
    except Exception as Error:
        # delete callbackQuery in an Exception [mainly if the original message has been deleted]
        await callbackQuery.message.delete()
        return "delete"


# SIZE FORMATER (TO HUMAN READABLE FORM) 
async def gSF(b, factor=2**10, suffix="B"):      # get_size_format
    try:
        for unit in ["", "K", "M", "G", "T"]:    # Scale bytes to its proper byte format
            if b < factor:                       # e.g: 1253656 => '1.20MB'
                return f"{b:.2f}{unit}{suffix}"  #      1253656678 => '1.17GB'
            b /= factor
        return f"{b:.2f}Y{suffix}"
    except Exception:
        pass


# CHECKS PDF CODEC, IS ENCRYPTED OR NOT
async def checkPdf(
    file_path: str, callbackQuery, lang_code: str = settings.DEFAULT_LANG
):
    try:
        CHUNK, _ = await translate(text = "PDF_MESSAGE", lang_code = lang_code)

        # open pdf file from file_path
        with fitz.open(file_path) as doc:
            pdfMetaData = (
                "".join(
                    f"`{i} : {doc.metadata[i]}`\n"
                    for i in doc.metadata
                    if doc.metadata[i] != ""
                )
                if doc.metadata
                else ""
            )
            if doc.is_encrypted:
                try:
                    await callbackQuery.edit_message_text(
                        text=CHUNK["encrypt"].format(
                            callbackQuery.message.reply_to_message.document.file_name,
                            await gSF(
                                callbackQuery.message.reply_to_message.document.file_size
                            ),
                        )
                        + "\n\n"
                        + CHUNK["pg"].format(doc.page_count)
                        + "\n\n"
                        + pdfMetaData,
                        reply_markup=await createBUTTON(CHUNK["encryptCB"], order=11),
                    )
                except Exception:
                    pass
                if callbackQuery.data != "work|decrypt":
                    await work(callbackQuery, "delete", False)
                return "encrypted", doc.page_count
            else:
                if callbackQuery.data != "#merge":
                    await callbackQuery.edit_message_text(
                        text=CHUNK["pdf"].format(
                            callbackQuery.message.reply_to_message.document.file_name,
                            await gSF(
                                callbackQuery.message.reply_to_message.document.file_size
                            ),
                        )
                        + "\n\n"
                        + CHUNK["pg"].format(doc.page_count)
                        + "\n\n"
                        + pdfMetaData,
                        reply_markup=callbackQuery.message.reply_markup,
                    )
                return "pass", doc.page_count
    # CODEC ERROR
    except Exception as Error:
        logger.exception("🐞 %s /close: %s" % (file_name, Error))
        await callbackQuery.edit_message_text(
            text=CHUNK["error"],
            reply_markup=await createBUTTON(CHUNK["errorCB"], order=11),
        )
        await work(callbackQuery, "delete", False)
        return "notPdf", "🚫"


# DOC. DOWNLOAD PROGRESS
# Here t = 0; cauz downloading using bot.downlod_media cant fetch
# total file size, so sharing file_size as function para.
async def progress(current, t, total, message, start):
    now = time.time()
    diff = now - start

    if round(diff % 10) in [0, 8] or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress = "[{0}{1}] \n".format(
            "".join(["●" for _ in range(math.floor(percentage / 5))]),
            "".join(["○" for _ in range(20 - math.floor(percentage / 5))]),
        )
        estimated_total_time = TimeFormatter(time_to_completion)
        lang_code = await getLang(message.chat.id)
        tTXT, tBTN = await translate(
            text="PROGRESS['progress']",
            button="DOCUMENT['cancelCB']",
            lang_code=lang_code,
        )
        tmp = progress + tTXT.format(
            await gSF(current),
            await gSF(total),
            await gSF(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        await message.edit_text(
            text="DOWNLOADING.. 📥\n{}".format(tmp)[:1000], reply_markup=tBTN
        )


# DOC. UPLOADING PROGRESS
async def _progress(
    current: int, total :int, message, start
) -> str:
    now = time.time()
    diff = now - start

    if round(diff % 10) in [0, 8] or current == total:
        await message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress = "[{0}{1}] \n".format(
            "".join(["●" for _ in range(math.floor(percentage / 5))]),
            "".join(["○" for _ in range(20 - math.floor(percentage / 5))]),
        )
        estimated_total_time = TimeFormatter(time_to_completion)
        lang_code = await getLang(message.chat.id)
        tTXT, tBTN = await translate(
            text="PROGRESS['progress']",
            button="DOCUMENT['cancelCB']",
            lang_code=lang_code,
        )
        tmp = progress + tTXT.format(
            await gSF(current),
            await gSF(total),
            await gSF(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        await message.edit_text(text="UPLOADING.. 📤\n{}".format(tmp), reply_markup=tBTN)


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


async def cbPRO(current, t, message, total=0, typ="DOWNLOADED", cancel=False):
    lang_code = await getLang(message.chat.id)
    if t != 0:
        total = t

    if typ == "DOWNLOADED":
        tTXT, _ = await translate(text="PROGRESS['cbPRO_D']", lang_code=lang_code)
    else:
        tTXT, _ = await translate(text="PROGRESS['cbPRO_U']", lang_code=lang_code)
    percentage = current * 100 / total
    if cancel:
        await message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(tTXT[0].format(percentage), callback_data="nabilanavab")
                ],[
                    InlineKeyboardButton(tTXT[1].format(percentage), callback_data="close|all")
                ]]
            )
        )
    else:
        await message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(tTXT[0].format(percentage), callback_data="close|all")
                ]]
            )
        )


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
