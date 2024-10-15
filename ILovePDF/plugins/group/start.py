# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab


file_name = "ILovePDF/plugins/group/start.py"

from plugins import *
from plugins.utils import *
from pyrogram.types import Message
from configs.config import images, dm
from pyrogram import Client as ILovePDF


@ILovePDF.on_message(filters.group & filters.incoming & filters.command("start"))
async def start(bot: ILovePDF, message: Message):
    """
        Handles the '/start' command for group messages.

        Args:
            bot: The bot instance.
            message: The incoming message containing the command.

        Returns:
            None
        """
    try:
        
        await message.reply_chat_action(enums.ChatAction.TYPING)
        
        # Retrieve the language code for the chat
        lang_code = await util.getLang(message.chat.id)

        # Translate the welcome text and button
        tTXT, tBTN = await util.translate(
            text = "HomeG['HomeA']",
            lang_code = lang_code,
            button = "HomeG['HomeACB']"
        )

        # Send a welcome photo with the translated caption and button
        await message.reply_photo(
            photo = images.WELCOME_PIC,
            caption = tTXT.format(
                message.chat.title, "𝐈 ❤️ 𝐏𝐃𝐅"
            ),
            reply_markup = tBTN,
            quote = False,
        )

        # Optionally delete the command message to keep the chat clean
        return await message.delete()
    
    except Exception as e:
        # Log the exception with a traceback for debugging
        logger.exception("🐞 %s: %s" % (fileName, e), exc_info = True)


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD