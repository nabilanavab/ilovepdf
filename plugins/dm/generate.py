# fileName : plugins/dm/generate.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: INFO
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.INFO,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )
# DISABLE PIL LOGGING MESSAGE [DEBUG] by changing to error
logging.getLogger("PIL.Image").setLevel(logging.ERROR)

import os
import shutil
import asyncio
from pdf import PDF
from .url import getPDF
from pyromod import listen
from pyrogram import filters
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from plugins.footer import footer, header
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#--------------->
#--------> REPLY TO /generate MESSAGE
#------------------->

@ILovePDF.on_message(
                    (filters.private | filters.group) &
                    filters.incoming &
                    filters.command(["generate"])
                    )
async def generate(bot, message):
    try:
        chat_id = message.chat.id
        # newName : new file name(/generate ___)
        newName = str(
                     message.text.replace("/generate", "")
                     )
        images = PDF.get(chat_id)
        if isinstance(images, list):
            pgnmbr = len(PDF[chat_id])
            del PDF[chat_id]
        
        # logger.info(images)
        # IF NO IMAGES SEND BEFORE
        if not images :
            await message.reply_chat_action(
                                           "typing"
                                           )
            imagesNotFounded = await message.reply_text(
                                                       "`No image founded.!!`😒"
                                                       )
            await asyncio.sleep(5)
            await message.delete()
            await imagesNotFounded.delete()
            return
        gnrtMsgId = await message.reply_text(
                                            f"`Generating pdf..`💚"
                                            )
        
        if newName == " name":
            fileName = f"{message.from_user.first_name}"+".pdf"
        elif len(newName) > 1 and len(newName) <= 45:
            fileName = f"{newName}"+".pdf"
        elif len(newName) > 45:
            fileName = f"{message.from_user.first_name}"+".pdf"
        else:
            fileName = f"{chat_id}"+".pdf"
        
        filePath = f"{message.chat.id}/{message.chat.id}.pdf"
        images[0].save(
                      filePath,
                      save_all = True,
                      append_images = images[1:]
                      )
        
        # Getting thumbnail
        thumbnail, fileName = await thumbName(message, fileName)
        if PDF_THUMBNAIL != thumbnail:
            location = await bot.download_media(
                                    message = thumbnail,
                                    file_name = f"{message.message_id}.jpeg"
                                    )
            thumbnail = await formatThumb(location)
        
        await gnrtMsgId.edit(
                            "`Uploading pdf.. `🏋️"
                            )
        await message.reply_chat_action(
                                       "upload_document"
                                       )
        with open(filePath, "rb") as pdf:
            logFile = await message.reply_document(
                                                  file_name = fileName,
                                                  document = pdf,
                                                  thumb = thumbnail,
                                                  caption = f"file Name: `{fileName}`\n"
                                                            f"`Total pg's: {pgnmbr}`"
                                                  )
        await gnrtMsgId.edit(
                            "`Successfully Uploaded.. `🤫"
                            )
        shutil.rmtree(f"{chat_id}")
        try:
            os.remove(location)
        except Exception: pass
        await footer(message, logFile)
    except Exception as e:
        logger.exception(
                        "/GENERATE:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            shutil.rmtree(f"{chat_id}")
        except Exception:
            pass

GEN = filters.create(lambda _, __, query: query.data.startswith("generate"))

@ILovePDF.on_callback_query(GEN)
async def _GEN(bot, callbackQuery):
    try:
        chat_id = callbackQuery.from_user.id
        
        images = PDF.get(chat_id)
        if isinstance(images, list):
            pgnmbr = len(PDF[chat_id])
            del PDF[chat_id]
        
        if not images :
            return await callbackQuery.answer(
                                             "No image founded.!! 😒"
                                             )
        await callbackQuery.answer()
        
        if callbackQuery.data[-3:] == "REN":
            fileName = await bot.ask(
                                    chat_id = chat_id,
                                    reply_to_message_id = callbackQuery.message.message_id,
                                    text = f"Now Send Me a New File Name 😒: ",
                                    reply_markup = ForceReply(True)
                                    )
            if (not fileName.text) or len(fileName.text)>50:
                fileName = f"{chat_id}.pdf"
            else:
                if fileName.text[-4:].lower() != ".pdf":
                    fileName = fileName.text + ".pdf"
                else:
                    fileName = fileName.text
        else:
            fileName = f"{chat_id}.pdf"
        
        gen = await callbackQuery.message.reply_text(
              f"File Name: `{fileName}`\nPages: `{pgnmbr}`",
              reply_markup = InlineKeyboardMarkup(
                                  [[
                                      InlineKeyboardButton(
                                                          "📚 GENERATING PDF..",
                                                          callback_data = "nabilanavab")
                                  ]]
             ),
             quote = False
             )
        filePath = f"{chat_id}/{callbackQuery.message.message_id}.pdf"
        images[0].save(
                      filePath,
                      save_all = True,
                      append_images = images[1:]
                      )
        
        # Getting thumbnail
        thumbnail, fileName = await thumbName(callbackQuery.message, fileName)
        if PDF_THUMBNAIL != thumbnail:
            location = await bot.download_media(
                                    message = thumbnail,
                                    file_name = f"{callbackQuery.message.message_id}.jpeg"
                                    )
            thumbnail = await formatThumb(location)
        
        await gen.edit_reply_markup(
              InlineKeyboardMarkup(
                                  [[
                                      InlineKeyboardButton(
                                                          "📤 ..UPLOADING..  📤",
                                                          callback_data = "nabilanavab")
                                  ]]
        ))
        await callbackQuery.message.reply_chat_action(
                                                     "upload_document"
                                                     )
        logFile = await callbackQuery.message.reply_document(
                                                            document = filePath,
                                                            caption = f"file Name: `{fileName}`\n"
                                                                      f"`Total pg's: {pgnmbr}`",
                                                            progress = getPDF,
                                                            file_name = fileName,
                                                            thumb = thumbnail,
                                                            progress_args = (
                                                                            gen, 0, 
                                                                            "UPLOADED"
                                                                            )
                                                            )
        await gen.delete()
        shutil.rmtree(f"{chat_id}")
        try:
            os.remove(location)
        except Exception: pass
        await footer(callbackQuery.message, logFile)
    except Exception as e:
        logger.exception(
                        "GENERATE/CALLBACK:CAUSES %s ERROR" %e,
                        exc_info=True
                        )
        try:
            shutil.rmtree(f"{chat_id}")
        except Exception:
            pass

#                                                                                 Telegram: @nabilanavab
