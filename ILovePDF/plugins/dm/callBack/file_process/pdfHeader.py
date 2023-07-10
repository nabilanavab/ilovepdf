# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/file_process/pdfHeader.py"

from fpdf import FPDF
from logger import logger
from pyromod import listen
from pyrogram import filters
from pyrogram.types import ForceReply


async def askText(bot, callbackQuery, question):
    try:
        newName = await bot.ask(
            chat_id=callbackQuery.from_user.id,
            reply_to_message_id=callbackQuery.message.id,
            text=question,
            filters=filters.text,
            reply_markup=ForceReply(True, "Enter Header/Footer.."),
        )
        return (True, newName) if newName.text != "/exit" else (False, newName)
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error


class header(FPDF):

    def header(self, text: str):
        self.set_font("Arial" , "U", 11)
        self.cell(0, 5, text, align="C", border=1)
        self.set_xy(0, 0)



async def pdfHeader(input_file: str, cDIR: str, text: str) -> (bool, str):
    """
    Adds Header to pdf files

    parameter:
        input_file : Here is the path of the file that the user entered
        text : header text

    return:
        bool        : Return True when the request is successful
        input_file : This is the path where the output file can be found.
    """
    try:
        output_path = f"{cDIR}/outPut.pdf"

        pdf = header()
        return True, output_path

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
