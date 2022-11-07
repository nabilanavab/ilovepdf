# fileName : plugins/dm/ban.py
# copyright ©️ 2021 nabilanavab

import asyncio
from logger import logger
from pyrogram import filters
from configs.config import dm
from pyrogram import Client as ILovePDF
from pyrogram.errors import ChatAdminRequired
from configs.db import dataBASE, BANNED_USR_DB, BANNED_GRP_DB
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid

if dataBASE.MONGODB_URI:
    from database import db

# =========================================================================================================> BANNED USER <=============================================
@ILovePDF.on_message(filters.incoming & filters.command('ban') &
                    filters.private & filters.user(dm.ADMINS))
async def _banUser(bot, message):
    try:
        if not dataBASE.MONGODB_URI:
            return await message.reply("Sry, Bot Don't have a DB", quote=True)
        procs = await message.reply("⚙️ `Processing..`",quote=True)
        await asyncio.sleep(1)
        if len(message.command) == 1:
            return await procs.edit("Give me a user id / username")
        reM = message.text.split(None)
        if len(reM) > 2:
            chat = message.text.split(None, 2)[1]
            reason = message.text.split(None, 2)[2]
        else:
            chat = message.command[1]
            reason = "oru chugam 😏"
        try:
            chat = int(chat)
        except Exception: pass    # if username [Exception]
        try:
            userINFO = await bot.get_users(chat)
        except PeerIdInvalid:
            return await procs.edit("This is an invalid user, make sure ia have met him before..")
        except IndexError:
            return await procs.edit("This might be a channel, make sure its a user..")
        except Exception as e:
            return await procs.edit(f"Error: `{e}`")
        else:
            if userINFO.id == 531733867:
                return await procs.edit(
                    f"Before Banning {userINFO.mention}.!\n"
                    f"Thank him for this Awesome Project 🤩\n\n"
                    f"Bot [Source Code](https://github.com/nabilanavab/iLovePDF) 😲"
                )
            elif (userINFO.id in dm.ADMINS):
                return await procs.edit(
                    f"I Never Ban {userINFO.mention}.. \n"
                    f"Reason: iCantBanBotADMIN 😏"
                )
            status = await db.get_key(id=userINFO.id, key="banned")
            if status:
                return await procs.edit(
                    f"{userINFO.mention} is already banned\n"
                    f"Reason: {status}"
                )
            await db.set_key(id=userINFO.id, key="banned", value=reason)
            BANNED_USR_DB.append(userINFO.id)
            await procs.edit(f"Successfully banned {userINFO.mention}")
    except Exception as e:
        logger.exception("/plugins/dm/banned/ban: %s" %(e), exc_info=True)

@ILovePDF.on_message(filters.incoming & filters.command('unban')
                    & filters.private & filters.user(dm.ADMINS))
async def _unbanUser(bot, message):
    try:
        if not dataBASE.MONGODB_URI:
            return await message.reply("Sry, Bot Don't have a DB", quote=True)
        procs = await message.reply("⚙️ `Processing..`", quote=True)
        await asyncio.sleep(1)
        if len(message.command) == 1:
            return await procs.edit("Give me a user id / username")
        reM = message.text.split(None)
        if len(reM) > 2:
            chat = message.text.split(None, 2)[1]
            reason = message.text.split(None, 2)[2]
        else:
            chat = message.command[1]
            reason = "No reason Provided"
        try:
            chat = int(chat)
        except Exception: pass
        try:
            userINFO = await bot.get_users(chat)
        except PeerIdInvalid:
            return await procs.edit("This is an invalid user, make sure ia have met him before..")
        except IndexError:
            return await procs.edit("This might be a channel, make sure its a user..")
        except Exception as e:
            return await procs.edit(f"Error: `{e}`")
        else:
            status = await db.get_key(id=userINFO.id, key="banned")
            logger.debug(userINFO.id)
            logger.debug(status)
            if not status:
                return await procs.edit(f"{userINFO.mention} is not yet banned.")
            await db.dlt_key(id=userINFO.id, key="banned")
            BANNED_USR_DB.remove(userINFO.id)
            await procs.edit(f"Successfully unbanned {userINFO.mention}")
    except Exception as e:
        logger.exception("/plugins/dm/banned/unban: %s" %(e), exc_info=True)

banUser = filters.create(lambda _, __, query: query.data.startswith(tuple(["banU|", "banC|"])))
@ILovePDF.on_callback_query(banUser)
async def _banUserCB(bot, callbackQuery):
    try:
        if callbackQuery.data.startswith("banU|"):
            chat_type = "user"
        else:
            chat_type = "chat"
        if callbackQuery.from_user.id not in dm.ADMINS:
            return await callbackQuery.answer("Message Not for U.. =(")
        userID = int(callbackQuery.data.split("|")[1])
        if userID == 531733867:
            return await callbackQuery.answer(
                f"Don't Even Think about banning\n\n𝙽𝙰𝙱𝙸𝙻  𝙰  𝙽𝙰𝚅𝙰𝙱\n\n"
                f"He's the master brain behind this project 😎", show_alert = True
            )
        elif userID in dm.ADMINS:
            return await callbackQuery.answer(
                f"I Never Ban Him.. 😏\nReason: iCantBanBotADMIN", show_alert = True
            )
        else:
            if chat_type == "user":
                if userID in BANNED_USR_DB:
                    return await callbackQuery.answer(f"He is already banned")
                await db.set_key(id=userID, key="banned", value="oru rasam.. 😝")
                BANNED_USR_DB.append(userID)
                _ = f"unbanU|{userID}"
            else:
                if userID in BANNED_GRP_DB:
                    return await callbackQuery.answer(f"chat is already banned")
                await db.set_key(id=userID, key="banned", value="oru rasam.. 😝", typ="group")
                BANNED_GRP_DB.append(userID)
                _ = f"unbanC|{userID}"
            
            await callbackQuery.answer(f"Successfully banned Him 😎")
            return await callbackQuery.message.edit_reply_markup(
                InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔴 UNB@N USER 🔴", callback_data=_)]]
                ))
    except Exception as e:
        logger.exception("/plugins/dm/banned/bancb %(e)s ERROR", exc_info=True)

unbanUser = filters.create(lambda _, __, query: query.data.startswith(tuple(["unbanU|", "unbanC|"])))
@ILovePDF.on_callback_query(unbanUser)
async def _unbanUserCB(bot, callbackQuery):
    try:
        if callbackQuery.data.startswith("unbanU|"):
            chat_type = "user"
        else:
            chat_type = "chat"
        if callbackQuery.from_user.id not in dm.ADMINS:
            return await callbackQuery.answer("Lesham Ulupp..")
        userID = int(callbackQuery.data.split("|")[1])
        
        if chat_type == "user":
            if userID not in BANNED_USR_DB:
                return await callbackQuery.answer(f"He is not yet banned")
            await db.dlt_key(id=userID, key="banned")
            BANNED_USR_DB.remove(userID)
            _ = f"banU|{userID}"
        else:
            if userID not in BANNED_GRP_DB:
                return await callbackQuery.answer("Not Banned yet")
            await db.dlt_key(id=userID, key="banned", typ="group")
            BANNED_GRP_DB.remove(userID)
            _ = f"banC|{userID}"
        
        await callbackQuery.answer(f"Successfully Unbanned Him 😎")
        return await callbackQuery.message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[InlineKeyboardButton("✅ B@N USER ✅", callback_data=_)]]
            ))
    except Exception as e:
        logger.exception("/pl/dm/banned/unbancb %s" %(e), exc_info=True)

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
