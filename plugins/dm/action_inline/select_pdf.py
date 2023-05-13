# fileName : plugins/dm/action_inline/select_pdf.py
# copyright ©️ 2021 nabilanavab

fileName = "plugins/dm/action_inline/select_pdf.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

from configs.log     import log
from .               import DATA
from logger          import logger
from pyrogram        import Client as ILovePDF
from pyrogram.types  import InlineKeyboardButton, InlineKeyboardMarkup

@ILovePDF.on_chosen_inline_result()
async def chosen_inline_result(bot, chosen_inline_result):
    try:
        lang_code = await getLang(inline_query.from_user.id)
        trCHUNK, _ = await translate(text="INLINE['edit']", lang_code=lang_code)
        
        data = DATA[chosen_inline_result.from_user.id][int(chosen_inline_result.result_id)]
        log_msg = await bot.send_photo(
            chat_id=int(log.LOG_CHANNEL), photo=data['thumb'], caption=data['caption'],
            reply_markup=InlineKeyboardMarkup(
                [[ InlineKeyboardButton("✅ B@N ✅", callback_data=f"banC|{chosen_inline_result.from_user.id}") ]]
            )
        )
        await bot.edit_inline_reply_markup(
            inline_message_id = chosen_inline_result.inline_message_id,
            reply_markup = InlineKeyboardMarkup(
                [[ InlineKeyboardButton(text=trCHUNK[0], callback_data=f"pD|{log_msg.id}|{chosen_inline_result.from_user.id}"),
                   InlineKeyboardButton(text=trCHUNK[1], switch_inline_query_current_chat=f"{chosen_inline_result.query}") ],
                 [ InlineKeyboardButton(text=trCHUNK[2], url="https://telegram.dog/ilovepdf_bot") ]]
            )
        )
        del DATA[chosen_inline_result.from_user.id]
        return
    
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info=True)

# Author: @nabilanavab
