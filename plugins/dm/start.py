# fileName : plugins/dm/start.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/start.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

import                             re
import                             os
import                             psutil
import                             shutil
import                             asyncio
from plugins.utils                 import *
from .photo                        import HD
from .callBack.file_process.link   import decode
from logger                        import logger
from .action_inline.in_bot         import openInBot
from pyrogram.enums      import ChatType
from lang.__users__      import userLang
from .settings           import _settings
from configs.db          import dataBASE, myID
from pyrogram.types      import InputMediaPhoto
from lang                import langList, disLang
from configs.config      import settings, images, dm
from pyrogram            import enums, filters, Client as ILovePDF
from pyrogram.types      import InlineKeyboardMarkup, InlineKeyboardButton

if dataBASE.MONGODB_URI:
    from database import db

# =============================| START MESSAGE |================================
async def extract_data(data):
    # extract lang_code, refer_id, get_pdf, md5_str from /start message if exist
    # eg: "/start +leng+r123456+gID+mMD5link"
    lang_code=re.search(r'\-l(\w+)\-', data)
    refer_id=re.search(r'\-r(\w+)\-', data)
    get_pdf=re.search(r'\-g(\w+)\-', data)
    md5_str=re.search(r'\-m(\w+)\-', data)
    return (
        lang_code.group(1) if lang_code else None,
        refer_id.group(1) if refer_id else None,
        get_pdf.group(1) if get_pdf else None,
        md5_str.group(1) if md5_str else None
    )

@ILovePDF.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot, message):
    try:
        if "-" in message.text:
            lang_code, refer_id, get_pdf, md5_str = await extract_data(f"{message.text}-")
        
        lang_code=await util.getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        if settings.MULTI_LANG_SUP and message.from_user.language_code and message.from_user.language_code!="en":
            change, _ = await util.translate(text="SETTINGS['chgLang']", lang_code=lang_code)
            _lang = { langList[lang][1]:f"set|lang|{lang}" for lang in langList if lang != lang_code }
            change.update(_lang); back, _ = await util.translate(text="SETTINGS['back'][1]", lang_code=lang_code)
            change.update(back); tBTN = await util.createBUTTON(btn=change, order=int(f"1{((len(change)-2)//3)*'3'}{(len(change)-2)%3}1"))
            tTXT, _ = await util.translate(text="SETTINGS['lang']", lang_code=lang_code)
        elif "-" in message.text and md5_str:
            return await openInBot(bot, message, md5_str)
        else:
            tTXT, tBTN = await util.translate(
                text="HOME['HomeA']", lang_code=lang_code, order=2121 if message.chat.id not in dm.ADMINS else 21221,
                button="HOME['HomeACB']" if message.chat.id not in dm.ADMINS else "HOME['HomeAdminCB']"
            )
        
        await message.reply_photo(
                                 photo=images.WELCOME_PIC, reply_markup = tBTN,
                                 caption=tTXT.format(message.from_user.mention, myID[0].mention),
                                 )
        await message.reply_sticker(
                                   sticker="CAACAgIAAxkBAAEVZ65kduZn7WTQXlyDFErYqb0BvyoIEQACVQADr8ZRGmTn_PAl6RC_LwQ",
                                   reply_markup=InlineKeyboardMarkup(
                                       [[ InlineKeyboardButton(text="🔎 SEARCH PDF 🔎", switch_inline_query_current_chat="" )]]
                                   ))
        if "-" in message.text and get_pdf:
            await decode(bot, get_pdf, message, lang_code)
        return await message.delete()
    except Exception as e:
        logger.exception("🐞 %s: %s" %(file_name, e), exc_info=True)

# =========================| START CALLBACK |================================
@ILovePDF.on_callback_query(filters.regex("^Home"))
async def home(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code, doc=False):
            return
        
        await callbackQuery.answer()
        data = callbackQuery.data
        home, page = callbackQuery.data.split("|")
        
        if page in ["A", "B2A"]:
            args = [callbackQuery.from_user.mention, myID[0].mention]
            if callbackQuery.message.chat.type == enums.ChatType.PRIVATE:
                if page == "B2A":
                    await callbackQuery.edit_message_media(InputMediaPhoto(images.WELCOME_PIC))
                tTXT, tBTN = await util.translate(
                    text="HOME['HomeA']", order = 2121,
                    button="HOME['HomeACB']" if callbackQuery.message.chat.id not in dm.ADMINS else "HOME['HomeAdminCB']",
                    lang_code=lang_code
                )
            else:
                tTXT, tBTN = await util.translate(
                    text="HomeG['HomeA']",
                    button="HomeG['HomeACB']" if callbackQuery.message.chat.id not in dm.ADMINS else "HOME['HomeAdminCB']",
                    lang_code=lang_code
                )
            return await callbackQuery.edit_message_caption(caption=tTXT.format(*args), reply_markup=tBTN)
        
        elif page in ["B", "B2S"]:
            return await _settings(bot, callbackQuery)
        
        elif page == "C":
            tTXT, tBTN = await util.translate(text="HOME['HomeC']", button="HOME['HomeCCB']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(caption=tTXT, reply_markup=tBTN)
        
        elif page == "D":
            tTXT, tBTN = await util.translate(text="HOME['HomeD']", button="HOME['HomeDCB']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(caption=tTXT, reply_markup=tBTN)
        
    except Exception as e:
        logger.exception("🐞 %s /home: %s" %(file_name, e), exc_info = True)

# ====================== SERVER UPDATES ==============
@ILovePDF.on_callback_query(filters.regex("^status"))
async def _status(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        _, __ = callbackQuery.data.split("|")
        
        if await render.header(bot, callbackQuery, lang_code, doc=False):
            return
        
        if __ in ["db", "users"] and not dataBASE.MONGODB_URI:
            tTXT, tBTN = await util.translate(text="STATUS_MSG['NO_DB']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)
        await callbackQuery.answer()
        
        if __ in "db":
            total_users = await db.total_users_count()
            total_chats = await db.total_chat_count()
            tTXT, tBTN = await util.translate(text="STATUS_MSG['DB']", button="STATUS_MSG['BACK']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(
                caption = tTXT.format(total_users, total_chats), reply_markup = tBTN
            )
        
        elif __ == "server":
            total, used, free = shutil.disk_usage(".")
            total = await gSF(total); used = await gSF(used); free = await gSF(free)
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            tTXT, tBTN = await util.translate(text="STATUS_MSG['SERVER']", button="STATUS_MSG['BACK']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(
                caption = tTXT.format(total, used, disk_usage, free, cpu_usage, ram_usage, len("a"), callbackQuery.message.id),
                reply_markup = tBTN
            )
        
        elif __ == "admin":
            msg, tBTN = await util.translate(text="STATUS_MSG['ADMIN']", button="STATUS_MSG['BACK']", lang_code=lang_code)
            for admin in dm.ADMINS:
                try:
                    userINFO = await bot.get_users(int(admin))
                    msg += f"\n {userINFO.mention}"
                except Exception: pass
            return await callbackQuery.message.edit(text = msg.format(len(dm.ADMINS)), reply_markup = tBTN)
        
        elif __ == "users":
            users = await db.get_all_users()
            tTXT, tBTN = await util.translate(
                text="STATUS_MSG['USERS']", button="STATUS_MSG['BACK']", lang_code=lang_code
            )
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
            tTXT, tBTN = await util.translate(
                text="STATUS_MSG['HOME']", button="STATUS_MSG['_HOME']",order=12121, lang_code=lang_code
            )
            return await callbackQuery.message.edit(text=tTXT, reply_markup=tBTN)
    
    except Exception as e:
        logger.exception("/SERVER:CAUSES %s ERROR" %(e), exc_info=True)
        logger.exception("🐞 %s /status: %s" %(file_name, e), exc_info = True)

# ======= CLOSE CALLBACK =========
@ILovePDF.on_callback_query(filters.regex("^close"))
async def _close(bot, callbackQuery):
    try:
        _, data = callbackQuery.data.split("|")
        if data == "admin":
            if callbackQuery.from_user.id in dm.ADMINS:
                return await callbackQuery.message.delete()
            else:
                return await callbackQuery.answer("🫡")
        
        if await render.header(bot, callbackQuery, doc=False):
            return
        
        if data == "me":    # deletes message & current work
            await callbackQuery.message.delete()
            return await work.work(callbackQuery, "delete", False)
        elif data == "hd":
            await callbackQuery.message.delete()
            del HD[callbackQuery.message.chat.id]
            return
        elif data == "mee":
            return await callbackQuery.message.delete()
        elif data == "all":
            if callbackQuery.message.chat.type == enums.ChatType.PRIVATE:
                await callbackQuery.message.delete()
                return await callbackQuery.message.reply_to_message.delete()
            if await work.work(callbackQuery, "check", False):
                lang_code = await util.getLang(callbackQuery.from_user.id)
                _, __ = await util.translate(text = "PROGRESS['workInP']", lang_code = lang_code)
                return await callbackQuery.answer(_)
            return await callbackQuery.message.delete()
        elif data == "P2I":
            lang_code = await util.getLang(callbackQuery.from_user.id)
            _, canceled = await util.translate(
                text = "INDEX['cancelCB']", button = "INDEX['_canceledCB']", lang_code = lang_code
            )
            await callbackQuery.answer(_)
            await callbackQuery.edit_message_reply_markup(canceled)
            return await work.work(callbackQuery, "delete", False)
        elif data == "dev":
            lang_code = await util.getLang(callbackQuery.from_user.id)
            _, __ = await util.translate(text = "cbAns", lang_code = lang_code)
            return await callbackQuery.answer(_[0])
    
    except Exception as e:
        logger.exception("🐞 %s /close: %s" %(file_name, e))

# Author: @nabilanavab
