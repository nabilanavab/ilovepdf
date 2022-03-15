# fileName : Plugins/dm/feedback.py
# copyright ©️ 2021 nabilanavab

from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup

#--------------->
#--------> config vars
#------------------->

BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> LOCAL VARIABLES
#------------------->

UCantUse = "For Some Reason You Can't Use This Bot 🛑"

feedbackMsg = "[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)"

button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "😉 Create your Own 😉",
                    url="https://github.com/nabilanavab/ilovepdf"
                )
            ]
       ]
    )

#--------------->
#--------> REPLY TO /feedback
#------------------->

@ILovePDF.on_message(filters.private & filters.command(["feedback"]) & ~filters.edited)
async def feedback(bot, message):
    try:
        await message.reply_chat_action("typing")
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse, reply_markup=button, quote=True
            )
            return
        await message.reply_text(
            feedbackMsg, disable_web_page_preview = True
        )
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
