# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)
auth = "nabil"

import fitz
from pyromod import listen
from pyrogram import filters
from pyrogram.types import ForceReply


async def askPassword(bot, callbackQuery, question, process: str):
    try:
        password = await bot.ask(
            chat_id=callbackQuery.from_user.id,
            reply_to_message_id=callbackQuery.message.id,
            text=question.format(process),
            filters=filters.text,
            reply_markup=ForceReply(True, "Enter Password.."),
        )
        return (True, password) if password.text != "/exit" else (False, password)
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error


async def encryptPDF(input_file: str, password: str, cDIR: str) -> (bool, str):
    try:
        """
        PDF encryption is a security feature that allows you to protect your PDF documents by
        encrypting their content to prevent unauthorized access or modification. Encryption is
        the process of converting plain text into a secret code to protect it from unauthorized access.

        parameter:
            input_file : Here is the path of the file that the user entered
            password   : Password entered by the user for pdf encryption
            cDIR       : This is the location of the directory that belongs to the specific user.

        return:
            bool        : Return True when the request is successful
            output_path : This is the path where the output file can be found.
        """
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            number_of_pages = iNPUT.page_count
            iNPUT.save(
                output_path,
                encryption=fitz.PDF_ENCRYPT_AES_256,  # strongest algorithm
                owner_pw=auth,
                user_pw=f"{password}",
                permissions=int(
                    fitz.PDF_PERM_ACCESSIBILITY
                    | fitz.PDF_PERM_PRINT
                    | fitz.PDF_PERM_COPY
                    | fitz.PDF_PERM_ANNOTATE
                ),
            )
        return True, output_path

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
