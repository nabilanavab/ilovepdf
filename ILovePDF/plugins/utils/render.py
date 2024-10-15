# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab


file_name = "ILovePDF/plugins/utils/render.py"

import fitz
from .util import *
from plugins import *
from .work import work
from pyrogram.types import Message
from configs.config import dm, settings
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType, ChatAction


# Checks the user for a callback query
async def header(
    bot, callbackQuery, lang_code: str = settings.DEFAULT_LANG, doc: bool = True
):
    """
    This function checks if a specific process needs to be executed 
    for callback queries, particularly in groups to avoid confusion
    and errors from multiple users.
    """
    try:
        if not doc:
            chat_type: str = callbackQuery.message.chat.type
            user_id: int = callbackQuery.from_user.id

            if (
                chat_type != ChatType.PRIVATE
                and user_id not in dm.ADMINS
            ):
                userStat = await bot.get_chat_member(
                    callbackQuery.message.chat.id, user_id
                )
                if userStat.status not in [
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.OWNER,
                ]:
                    _, __ = await translate(text = "BAN['cbNotU']", lang_code = lang_code)
                    await callbackQuery.answer(_, show_alert = True)

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
            chat_type != ChatType.PRIVATE
            and user_id != fileExist.from_user.id
            and user_id not in dm.ADMINS
        ):
            userStat = await bot.get_chat_member(
                callbackQuery.message.chat.id, user_id
            )
            
            if userStat.status not in [
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            ]:
                alert_message, __ = await translate(text = "BAN['cbNotU']", lang_code = lang_code)
                await callbackQuery.answer(alert_message, show_alert = True)

                return True
            
        return False
    
    except Exception as Error:
        # delete callbackQuery in an Exception [mainly if the original message has been deleted]
        await callbackQuery.message.delete()
        return "delete"


# SIZE FORMATER (TO HUMAN READABLE FORM) 
async def gSF(b: int, factor: int = 2**10, suffix: str = "B") -> str:
    """
    Convert a size in bytes to a human-readable format (e.g., KB, MB, GB).
    
    Args:
        b (int): Size in bytes.
        factor (int): Conversion factor (default is 1024).
        suffix (str): Suffix to append (default is "B").
        
    Returns:
        str: Formatted size as a string.
    """
    try:

        for unit in ["", "K", "M", "G", "T"]:    # Scale bytes to its proper byte format
            
            if b < factor:                       # e.g: 1253656 => '1.20MB'
                return f"{b:.2f}{unit}{suffix}"  #      1253656678 => '1.17GB'
            b /= factor

        return f"{b:.2f}Y{suffix}"
    
    except Exception as e:
        logger.exception("Error in gSF function: %s", e)
        return "0 B"  # Fallback in case of an error


# CHECKS PDF CODEC, IS ENCRYPTED OR NOT
async def checkPdf(
    file_path: str, callbackQuery, lang_code: str = settings.DEFAULT_LANG
):
    """
    Check if the PDF file is encrypted and extract its metadata.
    
    Args:
        file_path (str): Path to the PDF file.
        callbackQuery: Callback query object for editing messages.
        lang_code (str): Language code for translation (default is set in config).
        
    Returns:
        tuple: A tuple containing the status ("encrypted", "pass", or "notPdf") and page count or error message.
    """
    try:
        # Translate message chunks
        CHUNK, _ = await translate(text = "PDF_MESSAGE", lang_code = lang_code)

        replyMessage = callbackQuery.message.reply_to_message

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
                        text = CHUNK["encrypt"].format(
                            replyMessage.document.file_name,
                            await gSF(replyMessage.document.file_size),
                        )
                        + "\n\n" + CHUNK["pg"].format(doc.page_count)
                        + "\n\n" + pdfMetaData,
                        reply_markup = await createBUTTON(CHUNK["encryptCB"], order = 11),
                    )

                except Exception:
                    pass

                if callbackQuery.data != "work|decrypt":
                    await work(callbackQuery, "delete", False)

                return "encrypted", doc.page_count
            
            else:
                if callbackQuery.data != "#merge":
                    await callbackQuery.edit_message_text(
                        text = CHUNK["pdf"].format(
                            replyMessage.document.file_name,
                            await gSF(replyMessage.document.file_size),
                        )
                        + "\n\n" + CHUNK["pg"].format(doc.page_count)
                        + "\n\n" + pdfMetaData,
                        reply_markup = callbackQuery.message.reply_markup,
                    )

                return "pass", doc.page_count
            
    # CODEC ERROR
    except Exception as Error:
        logger.exception("🐞 %s /close: %s" % (file_name, Error))
        await callbackQuery.edit_message_text(
            text = CHUNK["error"],
            reply_markup = await createBUTTON(CHUNK["errorCB"], order = 11),
        )
        await work(callbackQuery, "delete", False)
        return "notPdf", "🚫"


# DOC. DOWNLOAD PROGRESS
# Here t = 0; cauz downloading using bot.downlod_media cant fetch
# total file size, so sharing file_size as function para.
async def progress(
        current: int, t: int, total: int, message, start: float
    ) -> None:
    """
    Updates the download progress of a document.

    Args:
        current (int): The current number of bytes downloaded.
        t (int): Placeholder for an unused parameter (can be removed if unnecessary).
        total (int): The total file size in bytes.
        message: The message object to update with progress.
        start (float): The timestamp when the download started.
    """
    now: int = time.time()
    diff: int = now - start

    if round(diff % 10) in [0, 8] or current == total:
        percentage = current * 100 / total
        speed = current / diff if diff > 0 else 0
        time_to_completion = round((total - current) / speed) * 1000
        
        # Progress bar representation
        progress = "[{0}{1}] \n".format(
            "".join(["●" for _ in range(math.floor(percentage / 5))]),
            "".join(["○" for _ in range(20 - math.floor(percentage / 5))]),
        )

        estimated_total_time = TimeFormatter(time_to_completion)
        lang_code = await getLang(message.chat.id)
        
        # Translate progress message
        tTXT, tBTN = await translate(
            text = "PROGRESS['progress']",
            button = "DOCUMENT['cancelCB']",
            lang_code = lang_code,
        )

        # Construct the message to be displayed
        tmp = progress + tTXT.format(
            await gSF(current),
            await gSF(total),
            await gSF(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )

        # Update the message with progress
        await message.edit_text(
            text = "DOWNLOADING.. 📥\n{}".format(tmp)[:1000],
            reply_markup = tBTN
        )


# DOC. UPLOADING PROGRESS
async def _progress(
    current: int, total :int, message, start: float
) -> str:
    now: int = time.time()
    diff: int = now - start

    if round(diff % 10) in [0, 8] or current == total:
        await message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        
        # Create a progress bar representation
        progress = "[{0}{1}] \n".format(
            "".join(["●" for _ in range(math.floor(percentage / 5))]),
            "".join(["○" for _ in range(20 - math.floor(percentage / 5))]),
        )

        # Format estimated time to completion
        estimated_total_time = TimeFormatter(time_to_completion)
        lang_code = await getLang(message.chat.id)

        # Translate the progress text and cancel button
        tTXT, tBTN = await translate(
            text = "PROGRESS['progress']",
            button = "DOCUMENT['cancelCB']",
            lang_code = lang_code,
        )

        # Prepare the temporary message to be sent
        tmp = progress + tTXT.format(
            await gSF(current),
            await gSF(total),
            await gSF(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        
        # Update the message with the current upload progress
        await message.edit_text(
            text = "UPLOADING.. 📤\n{}".format(tmp), reply_markup = tBTN
        )


def TimeFormatter(milliseconds: int) -> str:
    """
    Convert milliseconds into a human-readable format.

    Args:
        milliseconds (int): The time duration in milliseconds.

    Returns:
        str: A formatted string representing days, hours, minutes, seconds, and milliseconds.
    """
    # Convert milliseconds to seconds and the remaining milliseconds
    seconds, milliseconds = divmod(int(milliseconds), 1000)

    # Convert seconds to minutes and the remaining seconds
    minutes, seconds = divmod(seconds, 60)

    # Convert minutes to hours and the remaining minutes
    hours, minutes = divmod(minutes, 60)

    # Convert hours to days and the remaining hours
    days, hours = divmod(hours, 24)

    # Create a formatted string for the time components
    tmp = (
        ((str(days) + "d, ") if days else "")                   + # Add days if present
        ((str(hours) + "h, ") if hours else "")                 + # Add hours if present
        ((str(minutes) + "m, ") if minutes else "")             + # Add minutes if present
        ((str(seconds) + "s, ") if seconds else "")             + # Add seconds if present
        ((str(milliseconds) + "ms, ") if milliseconds else "")    # Add milliseconds if present
    )

    # Return the formatted string, removing the trailing comma and space
    return tmp[:-2]             # Exclude the last two characters (", ")


async def cbPRO(current, t, message, total = 0, typ = "DOWNLOADED", cancel = False) -> None:
    """
    Update the callback query with the progress of a download or upload.

    Args:
        current (int): The current amount of data downloaded or uploaded.
        t (int): Total size of the data to be processed. If 0, will default to the `total` parameter.
        message: The message object to update with progress.
        total (int, optional): Total size of the data. Defaults to 0.
        typ (str, optional): Type of progress ("DOWNLOADED" or "UPLOADED"). Defaults to "DOWNLOADED".
        cancel (bool, optional): Indicates whether the action was canceled. Defaults to False.
    """
    lang_code = await getLang(message.chat.id)

    # Set total size for progress calculation
    if t != 0:
        total = t
    
    # Translate the appropriate text based on the type of progress
    if typ == "DOWNLOADED":
        tTXT, _ = await translate(text = "PROGRESS['cbPRO_D']", lang_code = lang_code)
    else:
        tTXT, _ = await translate(text = "PROGRESS['cbPRO_U']", lang_code = lang_code)
    
    # Calculate the percentage of progress
    percentage = current * 100 / total

    # Update the message's reply markup based on whether the action is canceled
    if cancel:
        await message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        tTXT[0].format(percentage), callback_data = "nabilanavab"
                    )
                ],[
                    InlineKeyboardButton(
                        tTXT[1].format(percentage), callback_data = "close|all"
                    )
                ]]
            )
        )
        
    else:
        await message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        tTXT[0].format(percentage), callback_data = "close|all"
                    )
                ]]
            )
        )


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD