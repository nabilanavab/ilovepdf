# fileName : plugins/dm/admin.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import time
import shutil
import psutil
import asyncio
import datetime
from pdf import PROCESS
from pyrogram import filters
from configs.dm import Config
from configs.db import dataBASE
from pyrogram.types import Message
from configs.db import isMONGOexist
from configs.group import groupConfig
from configs.images import BANNED_PIC
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from plugins.fileSize import get_size_format as gSF
from configs.db import BANNED_USR_DB, BANNED_GRP_DB
from pyrogram.errors import (
                            InputUserDeactivated, UserNotParticipant,
                            FloodWait, UserIsBlocked, PeerIdInvalid 
                            )

if isMONGOexist:
    from database import db

#--------------->
#--------> config vars
#------------------->

ADMIN_GROUP_ONLY = groupConfig.ADMIN_GROUP_ONLY
BANNED_GROUP = groupConfig.BANNED_GROUP
ADMIN_GROUPS = groupConfig.ADMIN_GROUPS
BANNED_USERS = Config.BANNED_USERS
ADMIN_ONLY = Config.ADMIN_ONLY
ADMINS = Config.ADMINS

UCantUse = "Hey {}\nFOR SOME REASON YOU CANT USE THIS BOT :("

GroupCantUse = "{} NEVER EXPECT A GOOD RESPONSE FROM ME\n\nADMINS RESTRICTED ME FROM WORKING HERE.. 🤭"

button = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Create your Own Bot",
               url="https://github.com/nabilanavab/ilovepdf")
        ],[
            InlineKeyboardButton("Tutorial",
                                     url="t.me/ilovepdf_bot"),
            InlineKeyboardButton("Update Channel",
                             url="telegram.dog/ilovepdf_bot")
        ]]
    )

#--------------->
#--------> LOCAL FUNCTIONs
#------------------->

async def bannedUsers(_, __, message: Message):
    if (message.from_user.id in BANNED_USERS) or (
           (ADMIN_ONLY) and (message.from_user.id not in ADMINS)) or (
               (isMONGOexist) and (message.from_user.id in BANNED_USR_DB)):
        return True
    return False

banned_user=filters.create(bannedUsers)

async def bannedGroups(_, __, message: Message):
    if (message.chat.id in BANNED_GROUP) or (
           (ADMIN_GROUP_ONLY) and (message.chat.id not in ADMIN_GROUPS)) or (
               (isMONGOexist) and (message.chat.id in BANNED_GRP_DB)):
        return True
    return False

banned_group=filters.create(bannedGroups)

@ILovePDF.on_message(
                    filters.private &
                    banned_user &
                    filters.incoming
                    )
async def bannedUsr(bot, message):
    try:
        await message.reply_chat_action("typing")
        # IF USER BANNED FROM DATABASE
        if message.from_user.id in BANNED_USR_DB:
            ban = await db.get_ban_status(message.from_user.id)
            await message.reply_photo(
                                     photo = BANNED_PIC,
                                     caption = UCantUse.format(message.from_user.mention)+f'\n\nREASON: {ban["ban_reason"]}',
                                     reply_markup = button,
                                     quote = True
                                     )
            return
        #IF USER BANNED FROM CONFIG.VAR
        await message.reply_photo(
                                 photo = BANNED_PIC,
                                 caption = UCantUse.format(message.from_user.mention),
                                 reply_markup = button,
                                 quote = True
                                 )
    except Exception as e:
        logger.exception(
                        "BAN_USER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_message(
                    filters.group &
                    banned_group &
                    filters.incoming
                    )
async def bannedGrp(bot, message):
    try:
        await message.reply_chat_action("typing")
        if message.chat.id in BANNED_GRP_DB:
            ban = await db.get_ban_status(message.chat.id)
            toPin = await message.reply_photo(
                                           photo = BANNED_PIC,
                                           caption = GroupCantUse.format(message.chat.title)+f'\n\nREASON: {ban["ban_reason"]}',
                                           reply_markup = button,
                                           quote = True
                                           )
        else:
            toPin = await message.reply_photo(
                                      photo = BANNED_PIC,
                                      caption = GroupCantUse.format(message.chat.title),
                                      reply_markup = button,
                                      quote = True
                                      )
        try:
            await toPin.pin()
        except Exception:
            pass
        await bot.leave_chat(message.chat.id)
    except Exception as e:
        logger.exception(
                        "BANNED_GROUP:CAUSE %(e)s ERROR",
                        exc_info=True
                        )

# ❌ MESSAGE BROADCAST ❌
async def broadcast_messages(user_id, message, info):
    try:
        if info == "c":
            await message.copy(chat_id=user_id)
            return True, "Success"
        else:
            await message.forward(chat_id=user_id)
            return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message, info)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        logger.exception(
                        "BROADCAST:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        return False, "Error"

@ILovePDF.on_message(
                    filters.command("broadcast") &
                    filters.user(ADMINS) &
                    filters.private &
                    ~filters.edited &
                    filters.incoming
                    )
async def _broadcast(bot, message):
    try:
        procs = await message.reply(
                                   "⚙️ __Processing..__", quote=True
                                   )
        if not message.reply_to_message:
            return await procs.edit(
                                   "__Please Reply To A Messge__ 🤫"
                                   )
        if not isMONGOexist:
            return await procs.edit(
                                   "Sorry.! I can't remember my Userlist 😲"
                                   )
        await asyncio.sleep(1)
        if len(message.command) == 2:
            info = message.text.split(None, 2)[1]
            if info not in ["f", "c"]:
                return await procs.edit(
                                       "🥴 Syntax Error:\n\n"
                                       "`/broadcast f`: broadcast message [with quotes]\n"
                                       "`/broadcast c`: broadcast as copy [without quotes]"
                                       )
        else:
            return await procs.edit(
                                   "🥴 Syntax Error:\n\n"
                                   "`/broadcast f`: broadcast message [with quotes]\n"
                                   "`/broadcast c`: broadcast as copy [without quotes]"
                                   )
        users = await db.get_all_users()
        broadcast_msg = message.reply_to_message
        await procs.edit(
                        text = "__⚙️ Broadcasting your messages...__",
                        reply_markup = InlineKeyboardMarkup(
                              [[InlineKeyboardButton(
                                    "↩️ asForward ↩️" if info=="f" else "👀 asCopy 👀", callback_data="air"
                              )]]
                        ))
        start_time = time.time()
        total_users = await db.total_users_count()
        done = 0; blocked = 0; deleted = 0; failed = 0; success = 0
        async for user in users:
            iSuccess, feed = await broadcast_messages(int(user['id']), broadcast_msg, info)
            if iSuccess:
                success += 1
            elif iSuccess == False:
                if feed == "Blocked":
                    blocked+=1
                elif feed == "Deleted":
                    deleted += 1
                elif feed == "Error":
                    failed += 1
            done += 1
            await asyncio.sleep(2)
            if not done % 20:
                await procs.edit(
                                text = f"`Broadcast in progress:`\n"
                                       f"__Total Users:__ {total_users}\n"
                                       f"__Completed:__   {done} / {total_users}\n"
                                       f"__Success:__     {success}\n"
                                       f"__Blocked:__     {blocked}\n"
                                       f"__Deleted:__     {deleted}\n",
                                reply_markup = InlineKeyboardMarkup(
                                       [[InlineKeyboardButton(
                                            "↩️ asForward ↩️" if info=="f" else "👀 asCopy 👀", callback_data="air"
                                       )]]
                                ))
        time_taken=datetime.timedelta(seconds=int(time.time()-start_time))
        await procs.edit(
                        f"`Broadcast Completed:`\n"
                        f"__Completed in__ {time_taken} __seconds.__\n\n"
                        f"__Total Users:__ {total_users}\n"
                        f"__Completed:__   {done} / {total_users}\n"
                        f"__Success:__     {success}\n"
                        f"__Blocked:__     {blocked}\n"
                        f"__Deleted:__     {deleted}"
                        )
    except Exception as e:
        logger.exception(
                        "/BROADCAST:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_message(
                    filters.command("message") &
                    filters.user(ADMINS) &
                    filters.private &
                    ~filters.edited &
                    filters.incoming
                    )
async def _message(bot, message):
    try:
        procs = await message.reply(
                                   "⚙️ Processing..",
                                   quote = True
                                   )
        await asyncio.sleep(1)
        if not message.reply_to_message:
            return await procs.edit(
                                   "__Please Reply To A Message..__ 🤧"
                                   )
        if len(message.command) == 1:
            return await procs.edit(
                                   "Give me a user id / username"
                                   )
        reM = message.text.split(None)
        if len(reM) == 3:
            chat = message.text.split(None, 2)[2]
            info = message.text.split(None, 2)[1]
            if info not in ["c", "f"]:
                return await procs.edit(
                                       "__Please Use__ `c`:copy or `f`:forward"
                                       "\n__Nothing Else Is Supposed__"
                                       )
        else:
            chat = message.command[1]
            info = "c"
        try:
            chat = int(chat)
        except Exception: # if username [Exception]
            pass
        try:
            userINFO = await bot.get_users(chat)
        except Exception as e:
            return await procs.edit(
                                   f"__Can't forward message__"
                                   f"\n__REASON:__ `{e}`"
                                   )
        forward_msg = message.reply_to_message
        try:
            if info == "c":
                await forward_msg.copy(userINFO.id)
            else:
                await forward_msg.forward(userINFO.id)
        except Exception:
            return await procs.edit(
                                   f"__Can't forward message__"
                                   f"\n__REASON:__ `{e}`"
                                   )
        else:
            return await procs.edit(
                                   "Successfully forwarded"
                                   )
    except Exception as e:
        logger.exception(
                        "/MESSAGE:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# ❌ ADMIN COMMAND (/server) ❌
@ILovePDF.on_message(
                    filters.private &
                    filters.command(["server"]) &
                    filters.incoming &
                    filters.user(Config.ADMINS)
                    )
async def server(bot, message):
    try:
        total, used, free = shutil.disk_usage(".")
        total = await gSF(total); used = await gSF(used); free = await gSF(free)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        if isMONGOexist:
            total_users = await db.total_users_count()
            total_chats = await db.total_chat_count()
        else:
            total_users = "No DB"; total_chats="No DB"
        await message.reply_text(
                            text=f"**◍ Total Space     :** `{total}` \n"
                                 f"**◍ Used Space     :** `{used}({disk_usage}%)` \n"
                                 f"**◍ Free Space      :** `{free}` \n"
                                 f"**◍ CPU Usage      :** `{cpu_usage}`% \n"
                                 f"**◍ RAM Usage     :** `{ram_usage}`%\n"
                                 f"**◍ Current Work  :** `{len(PROCESS)}`\n"
                                 f"**◍ DB Users         :** `{total_users}`\n"
                                 f"**◍ DB Grups         :** `{total_chats}`\n"
                                 f"**◍ Message Id     :** `{message.message_id}`",
                            reply_markup = InlineKeyboardMarkup(
                                 [[
                                     InlineKeyboardButton("⟨ CLOSE ⟩",
                                            callback_data = "closeALL")
                                 ]]
                                 ),
                            quote=True
                            )
    except Exception as e:
        logger.exception(
                        "/SERVER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_message(
                    filters.command("admin") &
                    filters.user(ADMINS) &
                    filters.private &
                    ~filters.edited &
                    filters.incoming)
async def _adminList(bot, message):
    try:
        procs = await message.reply(
                                   "⚙️ Processing..",
                                   quote = True
                                   )
        await asyncio.sleep(1)
        msg = f"**Total ADMIN:** __{len(ADMINS)}__\n"
        await procs.edit(msg)
        for admin in ADMINS:
            try:
                userINFO = await bot.get_users(int(admin))
                msg += f"\n {userINFO.mention}"
            except Exception: pass
        await asyncio.sleep(1)
        await procs.edit(msg)
    except Exception as e:
        logger.exception(
                        "/ADMIN:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
#                                                                                                        Telegram: @nabilanavab
