# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/admin.py"

import datetime
from plugins import *
from pyrogram.errors import (
    InputUserDeactivated, UserNotParticipant,
    FloodWait, UserIsBlocked, PeerIdInvalid,
)
from configs.config import dm, settings
from configs.db import dataBASE, ping_list
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

if dataBASE.MONGODB_URI:
    from database import db


#  ADMIN MESSAGES 
@ILovePDF.on_message(
    filters.command("stop")
    & filters.user(dm.ADMINS)
    & filters.private
    & filters.incoming
)
async def stop(bot, message):
    try:
        settings.STOP_BOT = not settings.STOP_BOT
        reply = "`bot stoped..`" if settings.STOP_BOT else "`bot started..`"
        await message.reply(reply)
        if not settings.STOP_BOT:
            for user in ping_list:
                try:
                    await bot.send_message(
                        chat_id=user, text="`Bot Restarted..`"
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
    except Exception as error:
        logger.exception("🐞 %s: %s" % (file_name, error), exc_info=True)


@ILovePDF.on_callback_query(filters.regex("ping_me"))
async def ping_me(bot, callbackQuery):
    try:
        await callbackQuery.answer("👍")
        ping_me.append(callbackQuery.from_user.id)
    except Exception as error:
        logger.exception("🐞 %s: %s" % (file_name, error), exc_info=True)


#  ADMIN MESSAGES 
@ILovePDF.on_message(
    filters.command("send")
    & filters.user(dm.ADMINS)
    & filters.private
    & filters.incoming
)
async def sand(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        if not message.reply_to_message:
            error = await message.reply("⚙️ `Processing..`", quote=True)
            await asyncio.sleep(1)
            return await error.edit("__please, reply to A messge__ 🥲")

        msg = await message.reply_to_message.reply("⚙️ `Processing..`", quote=True)
        await message.delete()
        return await msg.edit(
            text="⚙️SEND MESSAGE: \n\n`Now, Select any Option Below.. `",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📢 ↓ BROADCAST ↓ 📢", callback_data="nabilanavab"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔸 COPY 🔸", callback_data="send|copy|broad"
                        ),
                        InlineKeyboardButton(
                            "🔸 FORWARD 🔸", callback_data="send|forw|broad"
                        ),
                    ],
                    [InlineKeyboardButton("👤 ↓ PM ↓ 👤", callback_data="nabilanavab")],
                    [
                        InlineKeyboardButton("🔸 COPY 🔸", callback_data="send|copy|pm"),
                        InlineKeyboardButton(
                            "🔸 FORWARD 🔸", callback_data="send|forw|pm"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        logger.exception("🐞 %s: %s" % (file_name, error), exc_info=True)


# ❌ MESSAGE BROADCAST ❌
async def broadcast_messages(user_id: int, message, info):
    try:
        if info == "copy":
            await message.copy(chat_id=user_id)
            return True, "Success"
        else:
            await message.forward(chat_id=user_id)
            return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, info)
    except InputUserDeactivated:
        # await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        return False, "Blocked"
    except PeerIdInvalid:
        # await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        logger.exception("🐞 %s: %s" % (file_name, e), exc_info=True)
        return False, "Error"


@ILovePDF.on_callback_query(filters.regex("^send"))
async def _send(bot, callbackQuery):
    try:
        data = callbackQuery.data
        _, __, ___ = callbackQuery.data.split("|")

        if ___ == "broad" and not dataBASE.MONGODB_URI:
            return await callbackQuery.answer("Can't Use this feature ={")

        await callbackQuery.answer("⚙️ Processing.. ")
        if ___ == "broad":
            users = await db.get_all_users()
            broadcast_msg = callbackQuery.message.reply_to_message
            total_users = await db.total_users_count()
            await callbackQuery.message.edit(
                text=f"⚙️ Started Broadcasting..\nTOTAL {total_users} USERS 😍\n\n↓ MESSAGE ↓"
                f"\n`{broadcast_msg.text if broadcast_msg.text else '📂 Media 📂'}`",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "🔸 asForward 🔸" if __ == "forw" else "🔸 asCopy 🔸", callback_data="nabilanavab",)
                    ]]
                ),
            )
            start_time = time.time()
            done = 0
            blocked = 0
            deleted = 0
            failed = 0
            success = 0

            async for user in users:
                iSuccess, feed = await broadcast_messages(
                    int(user["id"]), broadcast_msg, __
                )
                if iSuccess:
                    success += 1
                elif iSuccess == False:
                    if feed == "Blocked":
                        blocked += 1
                    elif feed == "Deleted":
                        deleted += 1
                    elif feed == "Error":
                        failed += 1
                done += 1
                await asyncio.sleep(1)
                if done % 20 == 0:
                    try:
                        await callbackQuery.message.edit_reply_markup(
                            InlineKeyboardMarkup(
                                [[
                                    InlineKeyboardButton(
                                        f"🔸 asForward({done*100}/{total_users}) 🔸"
                                        if __ == "forw"
                                        else f"🔸 asCopy({done*100/total_users}) 🔸",
                                        callback_data="nabilanavab")
                                ]]
                            )
                        )
                    except:
                        logger.debug("edit error - broadcast")
            time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
            return await callbackQuery.message.edit(
                text=f"`Broadcast Completed:`\n__Completed in__ {time_taken} __seconds ⏰__\n\n"
                f"__Total Users:__ {total_users} 😎\n__Completed:__   {done} / {total_users} 👑\n"
                f"__Success:__     {success} ✅\n__Blocked:__     {blocked} ❌\n"
                f"__Deleted:__     {deleted} ⚰️\n\n",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "🔸 asForward 🔸" if __ == "forw" else "🔸 asCopy 🔸", callback_data="nabilanavab",)
                    ]]
                ),
            )
        elif ___ == "pm":
            userID_msg = await bot.ask(
                text="__Now Send me the traget ID/Username__ 😅\n\n"
                "/exit for cancelling current process 🤐",
                chat_id=callbackQuery.from_user.id,
                reply_to_message_id=callbackQuery.message.id,
                reply_markup=ForceReply(True),
            )
            if not (userID_msg.text) or (userID_msg.text == "/exit"):
                await userID_msg.reply_to_message.delete()
                return await userID_msg.delete()

            chat = userID_msg.text
            try:
                chat = int(userID_msg.text)
            except Exception:  # if username [Exception]
                pass
            try:
                typ = "user"
                userINFO = await bot.get_users(chat)
            except Exception:
                typ = "group"
            if typ == "group":
                try:
                    userINFO = await bot.get_chat(chat)
                except Exception as e:
                    return await userID_msg.reply(
                        f"__Can't forward message__\n__REASON:__ `{e}`", quote=True
                    )
            forward_msg = callbackQuery.message.reply_to_message
            try:
                if __ == "copy":
                    await forward_msg.copy(userINFO.id)
                else:
                    await forward_msg.forward(userINFO.id)
            except Exception:
                return await userID_msg.reply(
                    f"__Can't forward message__\n__REASON:__ `{e}`"
                )
            else:
                return await userID_msg.reply("Successfully forwarded")
        else:
            return
    except Exception as e:
        logger.exception("🐞 %s: %s" % (file_name, e), exc_info=True)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
