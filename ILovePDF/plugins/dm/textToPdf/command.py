# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/textToPdf/command.py"

from plugins.utils import *


@ILovePDF.on_message(filters.private & filters.command(["txt2pdf"]) & filters.incoming)
async def text2PDF(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await util.getLang(message.chat.id)
        tTXT, tBTN = await util.translate(
            text="pdf2TXT['TEXT']",
            button="pdf2TXT['size_btn']",
            order=121,
            lang_code=lang_code,
        )
        await message.reply_photo(
            photo="https://graph.org/file/8b2073fb48283eddc4ebb.jpg",
            caption=tTXT,
            reply_markup=tBTN,
        )
        await message.delete()
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
