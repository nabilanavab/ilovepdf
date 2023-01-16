# fileName : plugins/dm/_init_.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/_init_.py"

from plugins.util         import *
from configs.config       import *
from configs.db           import *
from configs.log          import log
from pyrogram             import enums
from logger               import logger
from pyrogram.types       import Message
from plugins.util         import getLang
from pyrogram             import filters
from configs.db           import dataBASE
from lang                 import langList
from lang.__users__       import userLang
from pyrogram             import Client as ILovePDF
from pyrogram.errors      import UserNotParticipant

if dataBASE.MONGODB_URI:
    from database import db

# ==============================================================================================> BANNED USER <========================================================
async def bannedUsers(_, __, message: Message):
    if (message.from_user.id in dm.BANNED_USERS) or (
            (dm.ADMIN_ONLY) and (message.from_user.id not in dm.ADMINS)) or (
                (dataBASE.MONGODB_URI) and (message.from_user.id in BANNED_USR_DB)):
        return True
    return False
banned_user=filters.create(bannedUsers)
@ILovePDF.on_message(filters.private & banned_user & filters.incoming)
async def bannedUsr(bot, message):
    try:
        lang_code = await getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        # IF USER BANNED FROM DATABASE
        if message.from_user.id in BANNED_USR_DB:
            ban = await db.get_key(id=message.from_user.id, key="banned")
            trans_txt, trans_btn = await translate(text="BAN['UCantUseDB']", button="BAN['banCB']", lang_code=lang_code)
            return await message.reply_photo(
               photo = images.BANNED_PIC, reply_markup = trans_btn, quote = True,
               caption = trans_txt.format(message.from_user.mention, ban),
            )
        #IF USER BANNED FROM CONFIG.VAR
        trans_txt, trans_btn = await translate(text="BAN['UCantUse']", button="BAN['banCB']", lang_code=lang_code)
        return await message.reply_photo(
            photo = images.BANNED_PIC, reply_markup = trans_btn, quote = True,
            caption = trans_txt.format(message.from_user.mention),
        )
    except Exception as e:
        logger.exception("plugins/_init_: BAN_USER: %s" %(e), exc_info=True)

# ============================================================> BANNED GROUP <=========================================================================================
async def bannedGroups(_, __, message: Message):
    if (message.chat.id in group.BANNED_GROUP) or (
            (group.ADMIN_GROUP_ONLY) and (message.chat.id not in group.ADMIN_GROUPS)) or (
                (dataBASE.MONGODB_URI) and (message.chat.id in BANNED_GRP_DB)):
        return True
    return False
async def setDb(_, bot, message: Message):
    if (dataBASE.MONGODB_URI) and (message.chat.id not in GROUPS):
        await log.newUser(bot, message, False, False)
        GROUPS.append(message.chat.id)
    return True
banned_group=filters.create(bannedGroups)
set_db=filters.create(setDb)
@ILovePDF.on_message(filters.group & set_db & banned_group & filters.incoming)
async def bannedGrp(bot, message):
    try:
        lang_code = await getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        if message.chat.id in BANNED_GRP_DB:
            ban = await db.get_key(id=message.chat.id, key="banned", typ="group")
            trans_txt, trans_btn = await translate(text="BAN['GroupCantUseDB']", button="BAN['banCB']", lang_code=lang_code)
            toPin = await message.reply_photo(
                photo = images.BANNED_PIC, reply_markup = trans_btn, quote = True,
                caption = trans_txt.format(message.chat.title, ban)
            )
        else:
            trans_txt, trans_btn = await translate(text="BAN['GroupCantUse']", button="BAN['banCB']", lang_code=lang_code)
            toPin = await message.reply_photo(
                photo = images.BANNED_PIC, reply_markup = trans_btn,
                caption = trans_txt.format(message.chat.title), quote = True
            )
        try:
            await toPin.pin()
        except Exception: pass
        await bot.leave_chat(message.chat.id)
    except Exception as e:
        logger.exception("plugins/_init_: BANNED_GROUP: %s" %(e), exc_info=True)

# ====================================>  IF FORCE SUBSCRIPTION  <=====================================================================================================
async def notSubscribed(_, bot, message: Message):
    if message.text and message.text.startswith("/start"):
        msg = message.text.split(" ")
        if len(msg) != 1:
            index = msg[1].find("-l")
            lang = msg[1][index+2: index+5] if index != -1 else await getLang(message.chat.id)
            if lang in langList:
                userLang[message.chat.id] = lang
            # https://t.me/bot?start=-l{lang_code}-r{user_id}   referID Optional
            referID = msg[1].find("-r")
            if referID != -1:    # -1 coz it return -1 if not founded
                referID = msg[1][referID+2: ]
        else:
            referID = -1
        lang_code = await getLang(message.chat.id)
        if dataBASE.MONGODB_URI:               # CHECK IF USER IN DATABASE
            await log.newUser(bot, message, lang_code, int(referID))
        
    if len(invite_link) == 0:
        return False                             # IF FORCE SUB. TREAT AS SUBSCRIBED
    else:
        try:
            userStatus = await bot.get_chat_member(
                str(settings.UPDATE_CHANNEL), message.from_user.id
            )
            if userStatus.status == 'kicked':    # IF USER BANNED FROM CHANNEL
                return True
            return False
        except UserNotParticipant:
            return True
        except Exception as e:
            return True
not_subscribed=filters.create(notSubscribed)
@ILovePDF.on_message(filters.private & filters.incoming & not_subscribed)
async def non_subscriber(bot, message):
    try:
        lang_code = await getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        if message.text and message.text.startswith("/start") and "-g" in message.text:
            msg = message.text.split(" ")[1]
            code = msg.replace("-l", "-r").split("-r")[0]
        else:
            code = ""
        tTXT, tBTN = await translate(
            text="BAN['Force']", button="BAN['ForceCB']", asString=True, lang_code=lang_code
        )
        tBTN = await editDICT(inDir=tBTN, value=[invite_link[0], code])
        button = await createBUTTON(btn = tBTN, order="11")
        return await message.reply_photo(
            photo = images.WELCOME_PIC, quote = True,
            caption = tTXT.format(message.from_user.first_name, message.from_user.id), reply_markup = button
        )
    except Exception as e:
        logger.exception("plugins/_init_: FORCE_SUBSCRIPTION: %s" %(e), exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
