# fileName : plugins/dm/banned.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
from asyncio import sleep
from pyrogram import filters
from pyrogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup
                           )
from configs.dm import Config
from configs.db import isMONGOexist
from pyrogram import Client as ILovePDF
from pyrogram.errors import ChatAdminRequired
from configs.db import BANNED_USR_DB, BANNED_GRP_DB
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid

if isMONGOexist:
    from database import db


@ILovePDF.on_message(
                    filters.incoming &
                    filters.command('ban') &
                    filters.private & filters.user(Config.ADMINS)
                    )
async def _banUser(bot, message):
    try:
        if not isMONGOexist:
            await message.reply(
                               "Sry, Bot Don't have a DB",
                               quote = True
                               )
            return
        procs = await message.reply(
                                   "⚙️ Processing.",
                                   quote = True
                                   )
        await sleep(1)
        if len(message.command) == 1:
            return await procs.edit(
                                   "Give me a user id / username"
                                   )
        reM = message.text.split(None)
        if len(reM) > 2:
            chat = message.text.split(None, 2)[1]
            reason = message.text.split(None, 2)[2]
        else:
            chat = message.command[1]
            reason = "oru rasam 😏"
        try:
            chat = int(chat)
        except Exception: # if username [Exception]
            pass
        try:
            userINFO = await bot.get_users(chat)
        except PeerIdInvalid:
            return await procs.edit(
                                   "This is an invalid user, make sure ia have met him before.."
                                   )
        except IndexError:
            return await procs.edit(
                                   "This might be a channel, make sure its a user.."
                                   )
        except Exception as e:
            return await procs.edit(
                                   f"Error: `{e}`"
                                   )
        else:
            if userINFO.id == 531733867:
                return await procs.edit(
                                       f"Before Banning {userINFO.mention}.!\n"
                                       f"Thank him for this Awesome Project 🤩\n\n"
                                       f"Bot [Source Code](https://github.com/nabilanavab/iLovePDF) 😲"
                                       )
            elif (userINFO.id in Config.ADMINS):
                return await procs.edit(
                                       f"I Never Ban {userINFO.mention}.. \n"
                                       "Reason: iCantBanBotADMIN 😏"
                                       )
            status = await db.get_ban_status(userINFO.id)
            if status['is_banned']:
                return await procs.edit(
                                       f"{userINFO.mention} is already banned\n"
                                       f"Reason: {status['ban_reason']}"
                                       )
            await db.ban_user(userINFO.id, reason)
            BANNED_USR_DB.append(userINFO.id)
            await procs.edit(
                            f"Successfully banned {userINFO.mention}"
                            )
    except Exception as e:
        logger.exception(
                        "/BAN:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_message(
                    filters.incoming &
                    filters.command('unban') &
                    filters.private & filters.user(Config.ADMINS)
                    )
async def _unbanUser(bot, message):
    try:
        if not isMONGOexist:
            await message.reply(
                               "Sry, Bot Don't have a DB",
                               quote = True
                               )
            return
        procs = await message.reply(
                                 "⚙️ Processing",
                                 quote = True
                                 )
        await sleep(1)
        if len(message.command) == 1:
            return await procs.edit(
                                   "Give me a user id / username"
                                   )
        reM = message.text.split(None)
        if len(reM) > 2:
            chat = message.text.split(None, 2)[1]
            reason = message.text.split(None, 2)[2]
        else:
            chat = message.command[1]
            reason = "No reason Provided"
        try:
            chat = int(chat)
        except Exception:
            pass
        try:
            userINFO = await bot.get_users(chat)
        except PeerIdInvalid:
            return await procs.edit(
                                   "This is an invalid user, make sure ia have met him before.."
                                   )
        except IndexError:
            return await procs.edit(
                                   "This might be a channel, make sure its a user.."
                                   )
        except Exception as e:
            return await procs.edit(
                                   f"Error: `{e}`"
                                   )
        else:
            status = await db.get_ban_status(int(userINFO.id))
            logger.debug(userINFO.id)
            logger.debug(status)
            if not status['is_banned']:
                return await procs.edit(
                                       f"{userINFO.mention} is not yet banned."
                                       )
            await db.remove_ban(userINFO.id)
            BANNED_USR_DB.remove(userINFO.id)
            await procs.edit(
                            f"Successfully unbanned {userINFO.mention}"
                            )
    except Exception as e:
        logger.exception(
                        "/UNBAN:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_message(
                    filters.private &
                    filters.command('users') &
                    filters.user(Config.ADMINS) & filters.incoming
                    )
async def _listUser(bot, message):
    try:
        if not isMONGOexist:
            await message.reply(
                               "Sry, Bot Don't have a DB",
                               quote = True
                               )
            return
        procs=await message.reply(
                                "Getting List Of Users"
                                )
        await sleep(2)
        users = await db.get_all_users()
        out = "Users Saved In DB Are:\n\n"
        await procs.edit(out)
        await sleep(2)
        async for user in users:
            out += f"[{user['name']}](tg://user?id={user['id']})"
            if user['ban_status']['is_banned']:
                out += '( Banned User )'
            out += '\n'
        try:
            await procs.edit(out)
        except MessageTooLong:
            await procs.delete()
            with open('users.txt', 'w+') as outfile:
                outfile.write(out)
            await message.reply_document(
                                        'users.txt',
                                        caption = "List Of Users",
                                        quote = True
                                        )
            os.remove("users.txt")
    except Exception as e:
        logger.exception(
                        "/USERS:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

banUser = filters.create(lambda _, __, query: query.data.startswith(tuple(["banU|", "banC|"])))

@ILovePDF.on_callback_query(banUser)
async def _banUserCB(bot, callbackQuery):
    try:
        if callbackQuery.data.startswith("banU|"):
            chat_type = "user"
        else:
            chat_type = "chat"
        if callbackQuery.from_user.id not in Config.ADMINS:
            return await callbackQuery.answer(
                                             "Lesham Ulupp.."
                                             )
        _, userID = callbackQuery.data.split("|")
        if int(userID) == 531733867:
            return await callbackQuery.answer(
                                             f"Don't Even Think about banning\n\n"
                                             f"𝙽𝙰𝙱𝙸𝙻  𝙰  𝙽𝙰𝚅𝙰𝙱\n\n"
                                             f"He's the master brain behind this project 😎",
                                             show_alert = True
                                             )
        elif int(userID) in Config.ADMINS:
            return await callbackQuery.answer(
                                             f"I Never Ban Him.. 😏\n"
                                             "Reason: iCantBanBotADMIN",
                                             show_alert = True
                                             )
        else:
            if chat_type == "user":
                if int(userID) in BANNED_USR_DB:
                    return await callbackQuery.answer(
                                                     f"He is already banned"
                                                     )
                await db.ban_user(
                                 int(userID),
                                 "oru rasam.. 😝"
                                 )
                BANNED_USR_DB.append(int(userID))
            
            else:
                if int(userID) in BANNED_GRP_DB:
                    return await callbackQuery.answer(
                                                     f"chat is already banned"
                                                     )
                await db.disable_chat(
                                     int(userID),
                                     "oru rasam.. 😝"
                                     )
                BANNED_GRP_DB.append(int(userID))
            
            await callbackQuery.answer(
                                      f"Successfully banned Him 😎"
                                      )
            return await callbackQuery.message.edit_reply_markup(
                         InlineKeyboardMarkup(
                                 [[
                                         InlineKeyboardButton(
                                                 "» UnB@n »",
                                                 callback_data = f"unbanU|{userID}"
                                                 )
                                 ]]
                         ))
    except Exception as e:
        logger.exception(
                        "/BAN_USER_CB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

unbanUser = filters.create(lambda _, __, query: query.data.startswith(tuple(["unbanU|", "unbanC|"])))

@ILovePDF.on_callback_query(unbanUser)
async def _unbanUserCB(bot, callbackQuery):
    try:
        if callbackQuery.data.startswith("unbanU|"):
            chat_type = "user"
        else:
            chat_type = "chat"
        if callbackQuery.from_user.id not in Config.ADMINS:
            return await callbackQuery.answer(
                                             "Lesham Ulupp.."
                                             )
        _, userID = callbackQuery.data.split("|")
        
        if chat_type == "user":
            if int(userID) not in BANNED_USR_DB:
                return await callbackQuery.answer(
                                                 f"He is not yet banned"
                                                 )
            await db.remove_ban(
                               int(userID)
                               )
            BANNED_USR_DB.remove(int(userID))
        else:
            if int(userID) not in BANNED_GRP_DB:
                return await callbackQuery.answer(
                                                 "Not Banned yet"
                                                 )
            await db.re_enable_chat(
                                   int(userID)
                                   )
            BANNED_USR_DB.remove(int(userID))
        
        await callbackQuery.answer(
                                  f"Successfully Unbanned Him 😎"
                                  )
        return await callbackQuery.message.edit_reply_markup(
                    InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                            "« B@N «",
                                            callback_data = f"rU18"
                                            )
                            ]]
                    ))
    except Exception as e:
        logger.exception(
                        "/UN_BAN_USER_CB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

rU18 = filters.create(lambda _, __, query: query.data == "rU18")

@ILovePDF.on_callback_query(rU18)
async def _rU18(bot, callbackQuery):
    try:
        await callbackQuery.answer(
                                  "Are You 18.? playing like a kind 😏"
                                  )
    except Exception as e:
        logger.exception(
                        "RU18:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                          Telegram: @nabilanavab
