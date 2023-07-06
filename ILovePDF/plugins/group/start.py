# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/group/start.py"

from plugins import *
from plugins.utils import *
from configs.config import images, dm


@ILovePDF.on_message(filters.group & filters.incoming & filters.command("start"))
async def start(bot, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        lang_code = await util.getLang(message.chat.id)

        tTXT, tBTN = await util.translate(
            text="HomeG['HomeA']", lang_code=lang_code, button="HomeG['HomeACB']"
        )
        await message.reply_photo(
            photo=images.WELCOME_PIC,
            caption=tTXT.format(message.chat.title, "𝐈 ❤️ 𝐏𝐃𝐅"),
            reply_markup=tBTN,
            quote=False,
        )
        return await message.delete()
    except Exception as e:
        logger.exception("🐞 %s: %s" % (fileName, e), exc_info=True)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
