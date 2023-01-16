# fileName : plugins/group/start.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/group/start.py"

from logger         import logger
from configs.config import images, dm
from plugins.util   import getLang, translate
from pyrogram       import enums, filters, Client as ILovePDF

@ILovePDF.on_message(filters.group & filters.incoming & filters.command("start"))
async def start(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await getLang(message.chat.id)
        
        tTXT, tBTN = await translate(
            text = "HomeG['HomeA']", lang_code = lang_code, button = "HomeG['HomeACB']"
        )
        await message.reply_photo(
            photo = images.WELCOME_PIC,
            caption = tTXT.format(message.chat.title, "𝐈 ❤️ 𝐏𝐃𝐅"),
            reply_markup = tBTN,
            quote = False
        )
        return await message.delete()
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
