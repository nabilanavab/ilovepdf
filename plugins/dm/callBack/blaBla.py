# fileName : plugins/dm/callBack/underDev.py
# copyright ©️ 2021 nabilanavab

from pdf import PROCESS
from pyrogram import filters
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

error = filters.create(lambda _, __, query: query.data == "error")
closeme = filters.create(lambda _, __, query: query.data == "closeme")
closeALL = filters.create(lambda _, __, query: query.data == "closeALL")
underDev = filters.create(lambda _, __, query: query.data == "underDev")
canceled = filters.create(lambda _, __, query: query.data == "canceled")
completed = filters.create(lambda _, __, query: query.data == "completed")
cancelP2I = filters.create(lambda _, __, query: query.data == "cancelP2I")
notEncrypted = filters.create(lambda _, __, query: query.data == "notEncrypted")


@ILovePDF.on_callback_query(underDev)
async def _underDev(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "This feature is Under Development ⛷️"
        )
    except Exception:
        pass


@ILovePDF.on_callback_query(error)
async def _error(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "Error annenn paranjille.. then what.. 😏"
        )
    except Exception:
        pass


@ILovePDF.on_callback_query(closeme)
async def _closeme(bot, callbackQuery):
    try:
        try:
            await callbackQuery.message.delete()
        except Exception:
            pass
        await callbackQuery.answer(
            "Process Canceled.. 😏"
        )
        PROCESS.remove(callbackQuery.message.chat.id)
    except Exception:
        pass


@ILovePDF.on_callback_query(notEncrypted)
async def _notEncrypted(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "File Not Encrypted.. 👀"
        )
    except Exception:
        pass


@ILovePDF.on_callback_query(closeALL)
async def _closeALL(bot, callbackQuery):
    try:
        await callbackQuery.message.delete()
        await callbackQuery.message.reply_to_message.delete()
    except Exception as e:
        print(e)


@ILovePDF.on_callback_query(cancelP2I)
async def _cancelP2I(bot, callbackQuery):
    try:
        await callbackQuery.message.edit_reply_markup(
            InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("💤 CANCELING.. 💤", callback_data="n")
                ]]
            )
        )
        PROCESS.remove(callbackQuery.message.chat.id)
    except Exception:
        pass


@ILovePDF.on_callback_query(canceled)
async def _canceled(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "Nothing Official About it.. 😅"
        )
    except Exception:
        pass


@ILovePDF.on_callback_query(completed)
async def _completed(bot, callbackQuery):
    try:
        await callbackQuery.answer(
            "🎉 Completed.. 🏃"
        )
    except Exception:
        pass
