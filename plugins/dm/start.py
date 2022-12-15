# fileName : plugins/dm/start.py
# copyright ©️ 2021 nabilanavab

import asyncio
from .photo import HD
from pdf import PROCESS
from logger import logger
import psutil, os, shutil
from .settings import _settings
from configs.db import dataBASE
from lang.__users__ import userLang
from plugins.render import header, gSF
from pyrogram.types import InputMediaPhoto
from plugins.util import getLang, translate
from configs.config import settings, images, dm
from pyrogram import enums, filters, Client as ILovePDF

if dataBASE.MONGODB_URI:
    from database import db

# ============================================================================================== START MESSAGE ========================================================
@ILovePDF.on_message(filters.incoming & filters.command("start"))
async def start(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await getLang(message.chat.id)
        tTXT, tBTN = await translate(
            text="HOME['HomeA']", lang_code=lang_code,
            button="HOME['HomeACB']" if message.chat.id not in dm.ADMINS else "HOME['HomeAdminCB']"
        )
        if message.chat.type == enums.ChatType.PRIVATE:
            await message.reply_photo(
                photo = images.WELCOME_PIC,
                caption = tTXT.format(message.from_user.first_name, message.from_user.id),
                reply_markup = tBTN
            )
            return await message.delete()
    except Exception as e:
        logger.exception("plugins/dm/start: %s" %(e), exc_info=True)

# ======================================================== START CALLBACK =============================================================================================
close = filters.create(lambda _, __, query: query.data.startswith("close"))
Home = filters.create(lambda _, __, query: query.data.startswith("Home"))
refresh = filters.create(lambda _, __, query: query.data == "refresh")
Status = filters.create(lambda _, __, query: query.data.startswith("status"))

@ILovePDF.on_callback_query(Home)
async def home(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        if (callbackQuery.message.chat.type != enums.ChatType.PRIVATE) and (
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                tTXT, tBTN = await translate(text="BAN['cbNotU']", lang_code=lang_code)
                return callbackQuery.answer(tTXT)
        
        await callbackQuery.answer()
        data = callbackQuery.data
        home, page = callbackQuery.data.split("|")
        
        if page == "A":
            args = [callbackQuery.from_user.first_name, callbackQuery.from_user.id]
            tTXT, tBTN = await translate(
                text="HOME['HomeA']", button="HOME['HomeACB']" if callbackQuery.message.chat.id not in dm.ADMINS else "HOME['HomeAdminCB']",
                lang_code=lang_code)
            return await callbackQuery.edit_message_caption(caption=tTXT.format(*args), reply_markup=tBTN)
        
        elif page in ["B", "B2S"]:
            return await _settings(bot, callbackQuery)
        
        elif page == "B2A":
            args = [callbackQuery.from_user.first_name, callbackQuery.from_user.id]
            await callbackQuery.edit_message_media(InputMediaPhoto(images.WELCOME_PIC))
            tTXT, tBTN = await translate(
                text="HOME['HomeA']", button="HOME['HomeACB']" if callbackQuery.message.chat.id not in dm.ADMINS else "HOME['HomeAdminCB']",
                lang_code=lang_code)
            return await callbackQuery.edit_message_caption(caption=tTXT.format(*args), reply_markup=tBTN)
        
        elif page == "C":
            tTXT, tBTN = await translate(text="HOME['HomeC']", button="HOME['HomeCCB']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(caption=tTXT, reply_markup=tBTN)
        
        elif page == "D":
            tTXT, tBTN = await translate(text="HOME['HomeD']", button="HOME['HomeDCB']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(caption=tTXT, reply_markup=tBTN)
        
    except Exception as e:
        logger.exception("plugins/dm/start/home: %s" %(e), exc_info=True)

# ======================================================================== SERVER UPDATES =============================================================================
@ILovePDF.on_callback_query(Status)
async def _status(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        _, __ = callbackQuery.data.split("|")
        
        if __ in ["db", "users"] and not dataBASE.MONGODB_URI:
            tTXT, tBTN = await translate(text="STATUS_MSG['NO_DB']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        await callbackQuery.answer()
        
        if __ in "db":
            total_users = await db.total_users_count()
            total_chats = await db.total_chat_count()
            tTXT, tBTN = await translate(text="STATUS_MSG['DB']", button="STATUS_MSG['BACK']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(
                caption = tTXT.format(total_users, total_chats), reply_markup = tBTN
            )
        
        elif __ == "server":
            total, used, free = shutil.disk_usage(".")
            total = await gSF(total); used = await gSF(used); free = await gSF(free)
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            tTXT, tBTN = await translate(text="STATUS_MSG['SERVER']", button="STATUS_MSG['BACK']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(
                caption = tTXT.format(total, used, disk_usage, free, cpu_usage, ram_usage, len(PROCESS), callbackQuery.message.id),
                reply_markup = tBTN
            )
        
        elif __ == "admin":
            msg, tBTN = await translate(text="STATUS_MSG['ADMIN']", button="STATUS_MSG['BACK']", lang_code=lang_code)
            for admin in dm.ADMINS:
                try:
                    userINFO = await bot.get_users(int(admin))
                    msg += f"\n {userINFO.mention}"
                except Exception: pass
            return await callbackQuery.message.edit(text = msg.format(len(dm.ADMINS)), reply_markup = tBTN)
        
        elif __ == "users":
            users = await db.get_all_users()
            tTXT, tBTN = await translate(text="STATUS_MSG['USERS']", button="STATUS_MSG['BACK']", lang_code=lang_code)
            await callbackQuery.message.edit(text=tTXT, reply_markup=tBTN)
            rollnumber = 0; text=""
            async for user in users:
                rollnumber += 1
                if rollnumber % 500 == 0 and rollnumber % 1000 != 0:
                    await asyncio.sleep(.5)
                    try: await callbackQuery.message.edit(text=f"{tTXT}.", reply_markup=tBTN)
                    except: pass
                elif rollnumber % 500 == 0 and rollnumber % 1000 == 0:
                    try: await callbackQuery.message.edit(text=tTXT, reply_markup=tBTN)
                    except: pass
                try:
                    text += f"[{user['name']}](tg://user?id={user['id']})"
                except Exception:
                    logger.debug(f"error user: {user}")
                if user.get("banned", False):
                    text += ' `Banned ⚠️`'
                text += '\n'
                if rollnumber % 100 == 0:
                    logger.debug(f"••• {text}")
                    with open('users.txt', 'w+') as outfile:
                        outfile.write(text)
                    text == ""
            with open('users.txt', 'w+') as outfile:
                outfile.write(text)
            await callbackQuery.message.reply_document('users.txt')
            os.remove("users.txt")
        
        elif __ == "home":
            tTXT, tBTN = await translate(
                text="STATUS_MSG['HOME']", button="STATUS_MSG['_HOME']",order=12121, lang_code=lang_code
            )
            return await callbackQuery.message.edit(text=tTXT, reply_markup=tBTN)
    
    except Exception as e:
        logger.exception("/SERVER:CAUSES %s ERROR" %(e), exc_info=True)

# ============================ CLOSE CALLBACK =========================================================================================================================
@ILovePDF.on_callback_query(close)
async def _close(bot, callbackQuery):
    try:
        _, data = callbackQuery.data.split("|")
        if data == "admin":
            if callbackQuery.from_user.id in dm.ADMINS:
                return await callbackQuery.message.delete()
            else:
                return await callbackQuery.answer("🫡")
        
        # header after admin message coz no reply message show error and dlt msg
        if await header(bot, callbackQuery):
            return
        
        if data == "me":    # deletes message & current work
            await callbackQuery.message.delete()
            PROCESS.remove(callbackQuery.from_user.id)
            return
        if data == "hd":
            await callbackQuery.message.delete()
            del HD[callbackQuery.message.chat.id]
            return
        if data == "mee":
            return await callbackQuery.message.delete()
        elif data == "all":
            await callbackQuery.message.delete()
            return await callbackQuery.message.reply_to_message.delete()
        elif data == "P2I":
            lang_code = await getLang(callbackQuery.from_user.id)
            _, canceled = await translate(text="pdf2IMG['cbAns']", button="pdf2IMG['canceledCB']", lang_code=lang_code)
            await callbackQuery.answer(_)
            await callbackQuery.edit_message_reply_markup(canceled)
            PROCESS.remove(callbackQuery.from_user.id)
            return
        
    except Exception as e:
        logger.exception("Plugin/start/close: %s" %(e), exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
