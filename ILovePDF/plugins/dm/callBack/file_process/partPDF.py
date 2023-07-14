# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/file_process/partPDF.py"

import os
from logger import logger
from pyrogram import filters
from pyrogram.types import ForceReply
from PyPDF2 import PdfWriter, PdfReader


async def askPartPdf(bot, callbackQuery, question, limit: int = None):
    try:
        splitData = await bot.ask(
            chat_id=callbackQuery.from_user.id,
            reply_to_message_id=callbackQuery.message.id,
            text=question,
            filters=filters.text,
            reply_markup=ForceReply(True, "Enter Split PDF data.."),
        )
        if splitData.text.startswith(":"):
            pgData = splitData.text.split(":")[1]
            if not pgData.isdigit():
                return False, (splitData, "NotInteger:PageNumberMustBeAnInt")
            if limit and int(pgData)>int(limit):
                return False, (splitData, "TypeANumberLessThanPageNumber")
        else:
            if not splitData.text.isdigit():
                return False, (splitData, "NotInteger:PageNumberMustBeAnInt")
            if limit and int(splitData.text)>int(limit):
                return False, (splitData, "TypeANumberLessThanPageNumber")
        return (True, splitData) if splitData.text != "/exit" else (False, splitData)
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error


async def partPDF(input_file: str, cDIR: str, part: list) -> (bool, list):
    """
     With this feature, you can specify the desired number of pages per part, and the
     PDF splitting tool will automatically divide the document accordingly. For example,
     if you have a 20-page PDF and want to split it into parts of 5 pages each,
     the tool will generate four separate PDF files, each containing five pages of the
     original document.

    parameter:
        input_file    : Here is the path of the file that the user entered
        cDIR          : This is the location of the directory that belongs to the specific user.
        split         : page numbers that the user requests

    return:
        bool        : Return True when the request is successful
        output_path : This is the path where the output file can be found.
    """
    try:
        input_pdf_obj = PdfReader(input_file)
        num_pages = int(len(input_pdf_obj.pages))
        start_page = 0

        if part.startswith(":"):
            part = int(part.split(":")[1])
            pages_per_part = num_pages // part  # Integer division
            remainder = num_pages % part

            for i in range(part):
                part_pdf = PdfWriter()

                # Calculate the end page for the current part
                end_page = start_page + pages_per_part

                # Adjust the end page if there's a remainder
                if remainder > 0:
                    end_page += 1
                    remainder -= 1

                # Add the pages to the current part
                for page_num in range(start_page, end_page):
                    part_pdf.add_page(input_pdf_obj.pages[page_num])

                # Save the current part to a file
                part_filename = f"{cDIR}/{i+1}.pdf"
                with open(part_filename, "wb") as part_file:
                    part_pdf.write(part_file)
                
                start_page = end_page  # Set the start page for the next part

        else:
            part = int(part)
            pages_per_part = num_pages // part  # Integer division
            remainder = num_pages % part

            for i in range(pages_per_part):
                part_pdf = PdfWriter()

                end_page = start_page + part

                for page_num in range(start_page, end_page):
                    part_pdf.add_page(input_pdf_obj.pages[page_num])

                part_filename = f"{cDIR}/{i+1}.pdf"
                with open(part_filename, "wb") as part_file:
                    part_pdf.write(part_file)

                start_page = end_page

            if remainder:
                part_pdf = PdfWriter()
                for page_num in range(start_page, num_pages):
                    part_pdf.add_page(input_pdf_obj.pages[page_num])

                part_filename = f"{cDIR}/{pages_per_part+1}.pdf"
                with open(part_filename, "wb") as part_file:
                    part_pdf.write(part_file)

        os.remove(input_file)
        return True, cDIR

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
