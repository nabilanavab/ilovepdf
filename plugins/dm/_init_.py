# fileName : plugins/dm/_init_.py
# copyright ©️ 2021 nabilanavab

from logger import logger
from plugins.util import *
from pyrogram import enums
from pyrogram import filters
from configs.db import dataBASE
from pyrogram import Client as ILovePDF
from configs.config import settings, group, dm, images
from configs.db import BANNED_USR_DB, BANNED_GRP_DB, invite_link
from pyrogram.types import Message; from pyrogram.errors import UserNotParticipant

if dataBASE.MONGODB_URI:
    from database import db

# =======================================================> BANNED USER <========================================================
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

# ============================================================> BANNED GROUP <==================================================
async def bannedGroups(_, __, message: Message):
    if (message.chat.id in group.BANNED_GROUP) or (
            (group.ADMIN_GROUP_ONLY) and (message.chat.id not in group.ADMIN_GROUPS)) or (
                (dataBASE.MONGODB_URI) and (message.chat.id in BANNED_GRP_DB)):
        return True
    return False
banned_group=filters.create(bannedGroups)
@ILovePDF.on_message(filters.group & banned_group & filters.incoming)
async def bannedGrp(bot, message):
    try:
        lang_code = await getLang(message.chat.id)
        await message.reply_chat_action(enums.ChatAction.TYPING)
        if message.chat.id in BANNED_GRP_DB:
            ban = await db.get_key(id=message.chat.id, key="banned", type="group")
            trans_txt, trans_btn = await translate(text="BAN['GroupCantUseDB']", button="BAN['banCB']", lang_code=lang_code)
            toPin = await message.reply_photo(
                photo = images.BANNED_PIC, reply_markup = trans_btn, quote = True,
                caption = trans_txt.format(message.chat.title, ban["ban_reason"])
            )
        else:
            trans_txt, trans_btn = await translate(text="BAN['GroupCantUse']", button="BAN['banCB']", lang_code=lang_code)
            toPin = await message.reply_photo(
                photo = images.BANNED_PIC, reply_markup = trans_btn,
                caption = GroupCantUse.format(message.chat.title), quote = True
            )
        try:
            await toPin.pin()
        except Exception: pass
        await bot.leave_chat(message.chat.id)
    except Exception as e:
        logger.exception("plugins/_init_: BANNED_GROUP: %s" %(e), exc_info=True)

# ===================================================>  IF FORCE SUBSCRIPTION  <================================================
async def notSubscribed(_, bot, message: Message):
    if len(invite_link) == 0:
        return False                             # IF FORCE SUB. TREAT AS SUBSCRIBED
    else:
        try:
            userStatus = await bot.get_chat_member(str(settings.UPDATE_CHANNEL), message.from_user.id)
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
        tTXT, tBTN = await translate(text="BAN['Force']", button="BAN['ForceCB']", asString=True, lang_code=lang_code)
        tBTN = await editDICT(inDir=tBTN, value=invite_link[0])
        button = await createBUTTON(btn = tBTN, order="11")
        return await message.reply_photo(
            photo = images.WELCOME_PIC, quote = True,
            caption = tTXT.format(message.from_user.first_name, message.from_user.id), reply_markup = button
        )
    except Exception as e:
        logger.exception("plugins/_init_: FORCE_SUBSCRIPTION: %s" %(e), exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
