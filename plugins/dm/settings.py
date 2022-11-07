# fileName : plugins/dm/settings.py
# copyright ©️ 2021 nabilanavab

import asyncio
from logger import logger
from plugins.util import *
from pyrogram import filters
from configs.db import dataBASE
from plugins.render import header
from lang import langList, disLang
from lang.__users__ import userLang
from pyrogram.enums import ChatType
from pyrogram import Client as ILovePDF
from pyrogram.types import InputMediaPhoto
from configs.config import dm, images, settings as set
from configs.db import CUSTOM_THUMBNAIL_U, CUSTOM_THUMBNAIL_C, DATA

if dataBASE.MONGODB_URI:
    from database import db

settings = filters.create(lambda _, __, query: query.data.startswith("set"))
@ILovePDF.on_callback_query(settings)
async def _settings(bot, callbackQuery):
    try:
        lang_code = await getLang(callbackQuery.message.chat.id)
        data = callbackQuery.data.split("|", 1)[1]
        
        if data == "B":        # Home|B will redirect to settings
            if not dataBASE.MONGODB_URI:
                defalt, _ = await translate(text="SETTINGS['default'][0]", lang_code=lang_code)
                args = [
                    f"{callbackQuery.from_user.mention}", f"{callbackQuery.from_user.id}",
                    f"@{callbackQuery.from_user.username}" if callbackQuery.from_user.username else "❌",
                    "❌", await disLang(lang_code), defalt, defalt, defalt, defalt ]
                await callbackQuery.edit_message_media(InputMediaPhoto(images.THUMBNAIL_URL))        # thumbnail [defalt]
            
            else:
                data = await db.get_user_data(callbackQuery.message.chat.id)
                if not data:    # if monogo data fetching fails
                     error, errorCB = await translate(text="SETTINGS['error']", button="SETTINGS['errorCB']", lang_code=lang_code)
                     return await callbackQuery.edit_message_caption(caption=error, reply_markup=errorCB)
                
                defalt, _ = await translate(text="SETTINGS['default']", lang_code=lang_code)
                args = [
                    f"{callbackQuery.from_user.mention}", f"{callbackQuery.from_user.id}",
                    f"@{callbackQuery.from_user.username}" if callbackQuery.from_user.username else "❌",
                    data['join_date'], await disLang(lang_code), f"`{data['api']}`" if data.get('api', 0) else defalt[0],
                    defalt[1] if data.get('thumb', 0) else defalt[0], f"`{data['capt']}`" if data.get('capt', 0) else defalt[0],
                    f"`{data['fname']}`" if data.get('fname', 0) else defalt[0] ]
                await callbackQuery.edit_message_media(InputMediaPhoto(data['thumb']) if data.get('thumb', 0) else InputMediaPhoto(images.THUMBNAIL_URL))   #thumb
            
            tTXT, tBTN = await translate(text="HOME['HomeB']", button="HOME['HomeBCB']", lang_code=lang_code)
            return await callbackQuery.edit_message_caption(caption=tTXT.format(*args), reply_markup=tBTN)
        
        if data == "B2S":        # from settings part function to settings
            _, tBTN = await translate(button="HOME['HomeBCB']", lang_code=lang_code)
            return await callbackQuery.message.edit_reply_markup(tBTN)
        
        if not data.startswith("lang") and not dataBASE.MONGODB_URI:
            tTXT, tBTN = await translate(text="STATUS_MSG['NO_DB']", lang_code=lang_code)
            return await callbackQuery.answer(tTXT)

        user_id = callbackQuery.from_user.id; chat_id = callbackQuery.message.chat.id; chat_type = callbackQuery.message.chat.type
        
        if chat_type != ChatType.PRIVATE:
            return await callbackQuery.answer()
        
        elif data.startswith("lang"):    # getLang
            if not set.MULTI_LANG_SUP:
                cant, _ = await translate(text="SETTINGS['cant']", lang_code=lang_code)
                return await callbackQuery.answer(cant)
            if data == "lang":
                change, _ = await translate(text="SETTINGS['chgLang']", lang_code=lang_code)
                _lang = { langList[lang][1]:f"set|lang|{lang}" for lang in langList if lang != lang_code }
                change.update(_lang); back, _ = await translate(text="SETTINGS['back']", lang_code=lang_code)
                change.update(back); change = await createBUTTON(btn=change, order=int(f"1{((len(change)-2)//3)*'3'}{(len(change)-2)%3}1"))
                tTXT, _ = await translate(text="SETTINGS['lang']", lang_code=lang_code); await callbackQuery.answer(tTXT)
                return await callbackQuery.message.edit_reply_markup(change)
            else:
                lang = data.split("|", 1)[1]; userLang[chat_id] = lang
                if dataBASE.MONGODB_URI:
                    if lang != set.DEFAULT_LANG:
                        await db.set_key(callbackQuery.message.chat.id, "lang", lang)
                    else:
                        await db.dlt_key(callbackQuery.message.chat.id, "lang")
            _, __ = await translate(text="SETTINGS['feedback']", button="SETTINGS['feedbtn']", lang_code=lang)
            await callbackQuery.message.reply_text(text=_.format(await disLang(lang)), reply_markup=__)
            
        elif data.startswith("thumb"):
            if data == "thumb":
                if user_id in CUSTOM_THUMBNAIL_U:
                    _, tBTN = await translate(button="SETTINGS['thumb'][1]", order=121, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
                else:
                    _, tBTN = await translate(button="SETTINGS['thumb'][0]", order=111, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
            elif data == "thumb+":    # add thumb
                tTXT, tBTN = await translate(text="SETTINGS['ask']", button="SETTINGS['wait']", order=111, lang_code=lang_code)
                await callbackQuery.edit_message_caption(caption=tTXT[0], reply_markup=tBTN)
                await asyncio.sleep(1)
                await callbackQuery.edit_message_caption(caption=tTXT[1], reply_markup=tBTN)
                getThumb = await bot.listen(user_id)
                if getThumb.photo:
                    await db.set_key(user_id, "thumb", getThumb.photo.file_id)
                    CUSTOM_THUMBNAIL_U.append(user_id)
                await getThumb.delete()
            elif data == "thumb-":   # delete thumb
                CUSTOM_THUMBNAIL_U.remove(user_id)
                await db.dlt_key(callbackQuery.message.chat.id, "thumb")
        
        elif data.startswith("api"):
            current = DATA.get(int(user_id), 0)
            if data == "api":        # DATA saved order ["api", "fname", "caption]
                if current and current[0]:
                    _, tBTN = await translate(button="SETTINGS['api'][1]", order=121, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
                else:
                    _, tBTN = await translate(button="SETTINGS['api'][0]", order=111, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
            elif data == "api+":
                tTXT, tBTN = await translate(text="SETTINGS['ask']", button="SETTINGS['waitApi']", order=111, lang_code=lang_code)
                await callbackQuery.edit_message_caption(caption=tTXT[0], reply_markup=tBTN)
                _, __ = await translate(text="SETTINGS['askApi']", lang_code=lang_code)
                await asyncio.sleep(1)
                await callbackQuery.edit_message_caption(caption=tTXT[1]+_, reply_markup=tBTN)
                getName = await bot.listen(user_id)
                if getName.text:
                    await db.set_key(user_id, "api", f"{getName.text}"[:60])
                    if current:
                        DATA[user_id][1] = True
                    else:
                        DATA[user_id] = [True, 0, 0]
                await getName.delete()
            elif data == "api-":
                DATA[user_id][0] = 0
                await db.dlt_key(callbackQuery.message.chat.id, "api")
        
        elif data.startswith("fname"):
            if set.DEFAULT_NAME:
                cant, _ = await translate(text="SETTINGS['cant']", lang_code=lang_code)
                return await callbackQuery.answer(cant)
            current = DATA.get(int(user_id), 0)
            if data == "fname":        # DATA saved order ["api", "fname", "caption]
                if current and current[1]:
                    _, tBTN = await translate(button="SETTINGS['fname'][1]", order=121, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
                else:
                    _, tBTN = await translate(button="SETTINGS['fname'][0]", order=111, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
            elif data == "fname+":
                tTXT, tBTN = await translate(text="SETTINGS['ask']", button="SETTINGS['wait']", order=111, lang_code=lang_code)
                await callbackQuery.edit_message_caption(caption=tTXT[0], reply_markup=tBTN)
                await asyncio.sleep(1)
                await callbackQuery.edit_message_caption(caption=tTXT[1], reply_markup=tBTN)
                getName = await bot.listen(user_id)
                if getName.text:
                    await db.set_key(user_id, "fname", f"{getName.text}"[:60])
                    if current:
                        DATA[user_id][1] = True
                    else:
                        DATA[user_id] = [0, True, 0]
                await getName.delete()
            elif data == "fname-":
                DATA[user_id][1] = 0
                await db.dlt_key(callbackQuery.message.chat.id, "fname")
        
        elif data.startswith("capt"):
            if set.DEFAULT_CAPT:
                cant, _ = await translate(text="SETTINGS['cant']", lang_code=lang_code)
                return await callbackQuery.answer(cant)
            current = DATA.get(int(user_id), 0)
            if data == "capt":        # DATA saved order ["api", "fname", "caption]
                if current and current[2]:
                    _, tBTN = await translate(button="SETTINGS['capt'][1]", order=121, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
                else:
                    _, tBTN = await translate(button="SETTINGS['capt'][0]", order=111, lang_code=lang_code)
                    return await callbackQuery.message.edit_reply_markup(tBTN)
            elif data == "capt+":
                tTXT, tBTN = await translate(text="SETTINGS['ask']", button="SETTINGS['wait']", order=111, lang_code=lang_code)
                await callbackQuery.edit_message_caption(caption=tTXT[0], reply_markup=tBTN)
                await asyncio.sleep(1)
                await callbackQuery.edit_message_caption(caption=tTXT[1], reply_markup=tBTN)
                getName = await bot.listen(user_id)
                if getName.text:
                    await db.set_key(user_id, "capt", f"{getName.text}"[:60])
                    if current:
                        DATA[user_id][2] = True
                    else:
                        DATA[user_id] = [0, 0, True]
                await getName.delete()
            elif data == "capt-":
                DATA[user_id][2] = 0
                await db.dlt_key(callbackQuery.message.chat.id, "capt")
        
        if not data.endswith("+"):    # for successful cbMGS, add wait for use & cb expires
            result, _ = await translate(text="SETTINGS['result'][1]", lang_code=lang_code)
            await callbackQuery.answer(result)
        await callbackQuery.edit_message_media(InputMediaPhoto(images.WELCOME_PIC))
        tTXT, tBTN = await translate(
            text="HOME['HomeA']", lang_code=lang if data.startswith("lang") else lang_code,
            button="HOME['HomeACB']" if callbackQuery.message.chat.id not in dm.ADMINS else "HOME['HomeAdminCB']"
        )
        return await callbackQuery.edit_message_caption(caption=tTXT.format(callbackQuery.from_user.first_name, callbackQuery.from_user.id), reply_markup=tBTN)
    
    except Exception as e:
        logger.debug(f"plugins/dm/callBack/settings : {e}", exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
