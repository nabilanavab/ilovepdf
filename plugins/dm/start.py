# fileName : plugins/dm/start.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

from pdf import invite_link
from pyrogram import filters
from configs.dm import Config
from plugins.footer import header
from plugins.dm.photo import images
from configs.images import FEEDBACK
from pyrogram import Client as ILovePDF
from plugins.dm.document import documents
from pyrogram.types import InputMediaPhoto
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from configs.db import isMONGOexist, LOG_CHANNEL
from configs.images import WELCOME_PIC, BANNED_PIC

if isMONGOexist:
    from database import db

#------------------->
#--------> LOCAL VARIABLES
#------------------->

welcomeMsg = """Hey [{}](tg://user?id={})..!!
This bot will helps you to do many things with pdf's 🥳

Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert PDF to images`
◍ `Convert files to pdf`"""

forceSubMsg = """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only Channel Members Can Use this Bot 🚶

This Means You Need To Join The Below Mentioned Channel for Using Me!

Hit on `"♻️retry♻️"` after joining.. 😅"""

helpMessage = """Hey  [{}](tg://user?id={}).!
Some of the main features are:

- Images to PDF:
    Images to PDF, [JPEG, png, JPG] files to PDF, Rename PDF at the Time Of Creation, Rename By Name

- PDF Manipulation:
    PDF to Images, PDF to JPEG, Fetch metaData, Merge Multiple PDF's, Split PDF's to parts, PDF to (messages, text, html, json), Zip / Rar PDF pages, Encrypt/Decrypt PDF, Add Stamps, OCR PDF, A4 Fotmatter, text to PDF, Get PDF Preview, Fetch Data From Protected Channels & Groups

- Convert Different Codecs to PDF
    ~ .epub, .fb2, .cbz, etc [with no limits]
    ~ 45 Other Codecs by Using convertAPI [linmited]

⚠️ WARNING ⚠️
◍ This Bot is Completely Free to Use. So, please dont spam here. Spamming is strictly prohibited and leads to permanent ban.🚶
"""

foolRefresh = "വിളച്ചിലെടുക്കല്ലേ കേട്ടോ 😐"

LOG_TEXT = "#newUser @kkhanyaseen\nID: {}\nView Profile: {}"
LOG_TEXT_C = "#newChat @kkhanyaseen\nID: {}\nGroup Title: {}\nTotal Users: {}\nUserNsme: {}"

button = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("📌 SET THUMB 📌",
                                 callback_data="getThumb"),
            InlineKeyboardButton("⚠️ HELP AND RULES ⚠️",
                                     callback_data="help")
        ],[
            InlineKeyboardButton("🤖 CHANNEL 🤖",
                  url="https://telegram.dog/ilovepdf_bot"),
            InlineKeyboardButton("📝 FEEDBACK 📝",
                                        url=f"{FEEDBACK}")
        ],[
            InlineKeyboardButton("➕ ADD TO GROUP ➕",
                                  callback_data="underDev")
        ],[
            InlineKeyboardButton("🚶 CLOSE 🚶",
                                    callback_data="close")
        ]]
    )

UPDATE_CHANNEL = Config.UPDATE_CHANNEL

#--------------->
#--------> /start (START MESSAGE)
#------------------->

@ILovePDF.on_message(
                    ~filters.edited &
                    filters.incoming &
                    filters.command(
                                   ["start", "ping"]
                    ))
async def start(bot, message):
    try:
        global invite_link
        await message.reply_chat_action(
                                       "typing"
                                       )
        # CHECK IF USER IN DATABASE
        if isMONGOexist:
            if message.chat.type in ['group', 'supergroup']:
                if not await db.is_chat_exist(message.chat.id):
                    await db.add_chat(
                                     message.chat.id,
                                     message.chat.title
                                     )
                    if LOG_CHANNEL:
                        try:
                            total = await bot.get_chat_members_count(
                                                                message.chat.id
                                                                )
                            await bot.send_message(
                                              chat_id = LOG_CHANNEL,
                                                  text = LOG_TEXT_C.format(
                                                                          message.chat.id,
                                                                          message.chat.title,
                                                                          total,
                                                                          message.chat.username if message.chat.username else "❌"
                                                                          ),
                                                   reply_markup = InlineKeyboardMarkup(
                                                          [[InlineKeyboardButton("« B@N «",
                                                                 callback_data = f"banC|{message.chat.id}")]]
                                                   ))
                        except Exception: pass
                try:
                    return await message.reply(
                                   f"Hi There.! 🖐️\n"
                                   f"Im new here {message.chat.title}\n\n"
                                   f"Let me Introduce myself.. \n"
                                   f"My Name is iLovePDF, and i can help you to do many "
                                   f"Manipulations with @Telegram PDF files\n\n"
                                   f"Thanks @nabilanavab for this Awesome Bot 😅", quote=True,
                                   reply_markup = InlineKeyboardMarkup(
                                                                     [[InlineKeyboardButton("🤠 BOT OWNER 🤠",
                                                                          url = "Telegram.dog/nabilanavab"),
                                                                       InlineKeyboardButton("🛡️ UPDATE CHANNEL🛡️",
                                                                          url = "Telegram.dog/iLovePDF_bot")],
                                                                      [InlineKeyboardButton("🌟 SOURCE CODE 🌟",
                                                                          url = "https://github.com/nabilanavab/iLovePDF")]]
                                  ))
                except Exception: pass
            if message.chat.type == "private":
                if not await db.is_user_exist(message.from_user.id):
                    await db.add_user(
                                     message.from_user.id,
                                     message.from_user.first_name
                                     )
                    if LOG_CHANNEL:
                        try:
                            await bot.send_message(
                                              chat_id = LOG_CHANNEL,
                                              text = LOG_TEXT.format(
                                                                    message.from_user.id,
                                                                    message.from_user.mention
                                                                    ),
                                              reply_markup = InlineKeyboardMarkup(
                                                          [[InlineKeyboardButton("« B@N «",
                                                          callback_data=f"banU|{message.from_user.id}")]]
                                              ))
                        except Exception: pass
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                userStatus = await bot.get_chat_member(
                                                      str(UPDATE_CHANNEL),
                                                      message.from_user.id
                                                      )
                # IF USER BANNED FROM CHANNEL
                if userStatus.status == 'banned':
                     await message.reply_photo(
                                              photo = BANNED_PIC,
                                              caption = "For Some Reason You Can't Use This Bot"
                                                        "\n\nContact Bot Owner 🤐",
                                              reply_markup = InlineKeyboardMarkup(
                                                             [[InlineKeyboardButton("🤠 OWNER 🤠",
                                                                 url = "https://t.me/nabilanavab")]]
                                              ))
                     return
            except Exception as e:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
                                                                   int(UPDATE_CHANNEL)
                                                                   )
                await message.reply_photo(
                                         photo = WELCOME_PIC,
                                         caption = forceSubMsg.format(
                                                                     message.from_user.first_name,
                                                                     message.from_user.id
                                                                     ),
                                         reply_markup = InlineKeyboardMarkup(
                                              [[
                                                      InlineKeyboardButton("🌟 JOIN CHANNEL 🌟",
                                                                    url = invite_link.invite_link)
                                              ],[
                                                      InlineKeyboardButton("♻️ REFRESH ♻️",
                                                                    callback_data = "refresh")
                                              ]]
                                         ))
                if message.chat.type not in ['group', 'supergroup']:
                    await message.delete()
                return
        # IF NO FORCE SUBSCRIPTION
        if message.chat.type == "private":
            await message.reply_photo(
                                     photo = WELCOME_PIC,
                                     caption = welcomeMsg.format(
                                                                message.from_user.first_name,
                                                                message.from_user.id
                                     ),
                                     reply_markup = button
                                     )
            await message.delete()
        else:
            await message.reply(
                               "THIS IS A WELCOME MESSAGE 😂\n\n"
                               "/help FOR HELP MESSAGE 🤧",
                               quote = True,
                               reply_markup = InlineKeyboardMarkup(
                                   [[
                                       InlineKeyboardButton("🌟 SOURCE CODE 🌟",
                                              url="https://github.com/nabilanavab/ILovePDF"),
                                       InlineKeyboardButton("🔍 ABOUT BOT 🔎",
                                                     url="https://telegram.dog/nabilanavab")
                                   ],[
                                       InlineKeyboardButton("📌 SET THUMB 📌",
                                                                   callback_data="getThumb")
                                   ]]
                               ))
    except Exception as e:
        logger.exception(
                        "PHOTO:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#--------------->
#--------> START CALLBACKS
#------------------->

refreshDoc = filters.create(lambda _, __, query: query.data == "refreshDoc")
refreshImg = filters.create(lambda _, __, query: query.data == "refreshImg")
refresh = filters.create(lambda _, __, query: query.data == "refresh")
close = filters.create(lambda _, __, query: query.data == "close")
back = filters.create(lambda _, __, query: query.data == "back")
hlp = filters.create(lambda _, __, query: query.data == "help")

@ILovePDF.on_callback_query(hlp)
async def _hlp(bot, callbackQuery):
    try:
        if (callbackQuery.message.chat.type != "private") and (
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                return callbackQuery.answer("Message Not For You.. 😏")
        
        await callbackQuery.answer()
        await callbackQuery.edit_message_caption(
              caption = helpMessage.format(
                        callbackQuery.from_user.first_name, callbackQuery.from_user.id
                        ),
                        reply_markup = InlineKeyboardMarkup(
                              [[InlineKeyboardButton("« BACK «",
                                       callback_data = "back")]]
              ))
    except Exception as e:
        logger.exception(
                        "HLP:CAUSES %(e)s ERROR",
                        exc_info = True
                        )

@ILovePDF.on_callback_query(back)
async def _back(bot, callbackQuery):
    try:
        if (callbackQuery.message.chat.type != "private") and (
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                return await callbackQuery.answer("Message Not For You.. 😏")
        
        await callbackQuery.answer()
        try:
            await callbackQuery.edit_message_media(InputMediaPhoto(WELCOME_PIC))
        except Exception: pass
        await callbackQuery.edit_message_caption(
              caption = welcomeMsg.format(
                        callbackQuery.from_user.first_name,
                        callbackQuery.message.chat.id
              ),
              reply_markup = button
              )
    except Exception as e:
        # error if back followed by help message
        logger.exception(
                        "BACK:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(refresh | refreshDoc | refreshImg)
async def _refresh(bot, callbackQuery):
    try:
        if (callbackQuery.message.chat.type != "private") and (
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                return await callbackQuery.answer("Message Not For You.. 😏")
        
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        userStatus = await bot.get_chat_member(
                                              str(UPDATE_CHANNEL),
                                              callbackQuery.from_user.id
                                              )
        await callbackQuery.answer()
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        if callbackQuery.data == "refresh":
            return await callbackQuery.edit_message_caption(
                          caption = welcomeMsg.format(
                                      callbackQuery.from_user.first_name,
                                      callbackQuery.from_user.id
                                      ),
                                      reply_markup = button
                         )
        if callbackQuery.data == "refreshDoc":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return await documents(
                            bot, messageId
                            )
        if callbackQuery.data == "refreshImg":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return await images(
                               bot, messageId
                               )
    except Exception as e:
        try:
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                                           callbackQuery.id,
                                           text = foolRefresh,
                                           show_alert = True,
                                           cache_time = 0
                                           )
        except Exception:
            pass

@ILovePDF.on_callback_query(close)
async def _close(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.message.delete()
    except Exception as e:
        logger.exception(
                        "CLOSE:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
