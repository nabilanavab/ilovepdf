# fileName: plugins/dm/action_inline/default_ans.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/action_inline/default_ans.py"

from plugins.utils   import *
from configs.db      import myID
from configs.config  import images
from lang            import langList
from pyrogram.types  import (InputTextMessageContent, InlineKeyboardMarkup,
                             InlineKeyboardButton, InlineQueryResultPhoto)

async def default_ans(inline_query) -> list:
    try:
        lang_code = await util.getLang(inline_query.from_user.id)
        CHUNK, _ = await util.translate(text="INLINE", lang_code=lang_code)
        
        # Getting Lang Data..
        BUTTON=CHUNK['lang_b']
        _lang = { langList[lang][1]:f"https://t.me/{myID[0].username}?start=#l{lang}#r{inline_query.from_user.id}" for lang in langList }
        BUTTON.update(_lang)
        BUTTON.update({"♻" : "-|refresh"})
        BUTTON = await util.createBUTTON(
            btn=BUTTON, order=int(f"1{((len(BUTTON)-2)//3)*'3'}{(len(BUTTON)-2)%3}1")
        )
        
        openChat = InlineKeyboardMarkup(
            [[ InlineKeyboardButton(text=CHUNK['openBot'], url=f"https://t.me/{myID[0].username}?start=#r{inline_query.from_user.id}") ]]
        )
        
        answer = [
            InlineQueryResultPhoto(
                photo_url="https://graph.org/file/e0543a5ace611768e71d1.jpg",
                title=CHUNK['sear_t'], input_message_content=InputTextMessageContent(CHUNK['sear_d']),
                reply_markup=InlineKeyboardMarkup(
                    [[ InlineKeyboardButton(text=CHUNK['search'], switch_inline_query_current_chat="" )]] ),
            ),
            InlineQueryResultPhoto(
                photo_url="https://graph.org/file/4506c172bf757ce187fe1.jpg",
                title=CHUNK['lang_t'], reply_markup=BUTTON, input_message_content=InputTextMessageContent(CHUNK['lang_d'])
            ),
            InlineQueryResultPhoto(
                photo_url="https://graph.org/file/521e4aa2469427281bfac.jpg",
                title=CHUNK['P2J_t'], reply_markup=openChat, input_message_content=InputTextMessageContent(CHUNK['P2J_d']),
            ),
            InlineQueryResultPhoto(
                photo_url="https://graph.org/file/178e9f143814f695578fc.jpg",
                title=CHUNK['lock_t'], reply_markup=openChat, input_message_content=InputTextMessageContent(CHUNK['lock_t']),
            ),
            InlineQueryResultPhoto(
                photo_url="https://graph.org/file/e4baa95ecfd27b8dc1407.jpg",
                title=CHUNK['save_t'], reply_markup=openChat, input_message_content=InputTextMessageContent(CHUNK['save_d']),
            ),
            InlineQueryResultPhoto(
                photo_url="https://graph.org/file/521e4aa2469427281bfac.jpg",
                title=CHUNK['P2J_t'], reply_markup=openChat, input_message_content=InputTextMessageContent(CHUNK['P2J_d']),
            ),
        ]
        
        return answer
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(fileName, Error), exc_info = True)
