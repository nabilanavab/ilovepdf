# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

from pyromod import listen
from pyrogram.types import ForceReply


async def askName(bot, callbackQuery, question):
    try:
        newName = await bot.ask(
            chat_id=callbackQuery.from_user.id,
            reply_to_message_id=callbackQuery.message.id,
            text=question,
            filters=filters.text,
            reply_markup=ForceReply(True, "Enter new File Name.."),
        )
        return (True, newName) if newName.text != "/exit" else (False, newName)
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error


async def renamePDF(input_file: str):
    """
    Renaming PDF files can help you keep your files organized and easy to find.
    By giving the file a descriptive name that reflects its contents, you can
    quickly identify the file you need without having to open it.

    parameter:
        input_file : Here is the path of the file that the user entered

    return:
        bool        : Return True when the request is successful
        input_file : This is the path where the output file can be found.
    """
    return True, input_file

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
