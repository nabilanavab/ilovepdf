# fileName : plugins/dm/action_inline/get_pdf.py
# copyright ©️ 2021 nabilanavab

fileName = "plugins/dm/action_inline/get_pdf.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from configs.log          import log
from plugins.utils.work   import work
from logger               import logger
from pyrogram             import Client as ILovePDF, filters
from pyrogram.types       import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument

async def download(name, download_link, bot, callbackQuery):
    try:
        response = requests.get(download_link, stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        block_size, current, percent = 1024, 0, 0
        cDIR = await work(callbackQuery, "check", False)
        if not cDIR:
            return await bot.edit_inline_reply_markup(
                inline_message_id = callbackQuery.inline_message_id,
                reply_markup = InlineKeyboardMarkup(
                    [[ InlineKeyboardButton( "♻️ TRY AGAIN ♻️", callback_data = f"{callbackQuery.data}" ) ]]
                ))
        path = f"{cDIR}/{name}"
        with open(path, "wb") as f:
            for data in response.iter_content(block_size):
                if not await work(callbackQuery, "check", False):
                    return False
                current = current + len(data)
                f.write(data)
                if int(current/total_size*10) > int(percent):
                    percent = int(current/total_size*10)
                    await bot.edit_inline_reply_markup(
                        inline_message_id = callbackQuery.inline_message_id,
                        reply_markup = InlineKeyboardMarkup(
                            [[ InlineKeyboardButton( "📥 DOWNLOADED {:.2f}% 📥".format(current/total_size * 100 ), callback_data = f"{callbackQuery.data}" ) ],[
                                InlineKeyboardButton( "🗑️ CANCEL 🗑️", callback_data = f"c{callbackQuery.data[1:]}" ) ]]
                        ))
        return path
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)
        return False

getPDF = filters.create(lambda _, __, query: query.data.startswith("legranchi"))

@ILovePDF.on_callback_query(getPDF)

async def pdfDriver(bot, callbackQuery):
    try:
        lang_code = await getLang(inline_query.from_user.id)
        trCHUNK, _ = await translate(text="INLINE", lang_code=lang_code)
        
        if not ( callbackQuery.from_user.id == int(callbackQuery.data.split("|")[2]) ):
            return await callbackQuery.answer(trCHUNK['cbNotU'])
        
        getMSG = await bot.get_messages(
            chat_id = int(log.LOG_CHANNEL),
            message_ids = int(callbackQuery.data.split("|")[1])
        )
        
        if getMSG.empty:
            return await callbackQuery.answer(trCHUNK['old'])
        
        if await work(callbackQuery, "check", False):
            return await callbackQuery.answer(trCHUNK['inWork'])
        await work(callbackQuery, "create", False)
        
        md5 = getMSG.caption.splitlines()[0].split(':')[1].strip()
        await book_process(m, md5)
        
        await bot.edit_inline_reply_markup(
            inline_message_id = callbackQuery.inline_message_id,
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton( "🍪 COOKING DATA 🍪", callback_data = f"{callbackQuery.data}" ) ],[
                   InlineKeyboardButton( "🗑️ CANCEL 🗑️", callback_data = f"c{callbackQuery.data[1:]}" ) ]]
            )
        )
        
        await bot.edit_inline_media(
            inline_message_id = callbackQuery.inline_message_id,
            media = InputMediaDocument(
                media = download_link if telegram_can else path,
                caption = getMSG.caption.split("°")[1]
            ),
            reply_markup = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        text = "♻️ SEARCH AGAIN ♻️",
                        switch_inline_query_current_chat = ""
                    )
                ]]
            )
        )
        return await work(callbackQuery, "delete", False)
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
        await work(callbackQuery, "delete", False)


closeDRIVE = filters.create(lambda _, __, query: query.data.startswith("cD|"))
@ILovePDF.on_callback_query(closeDRIVE)
async def close(bot, callbackQuery):
    try:
        if not (callbackQuery.from_user.id == int(callbackQuery.data.split("|")[2])):
            return await callbackQuery.answer("message not for you..")
        
        await callbackQuery.answer("🗑️")
        await work(callbackQuery, "delete", False)
    except Exception: pass
# Author: @nabilanavab
