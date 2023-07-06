# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

import fitz
from plugins.utils import *
from pyrogram.errors import FloodWait


async def messagePDF(
    input_file: str, cDIR: str, callbackQuery, dlMSG, text: str
) -> (bool, str):
    """
    The function takes the file path of a PDF file as input and returns the extracted text from the PDF file as output..

    parameter:
        input_file    : Here is the path of the file that the user entered
        cDIR          : This is the location of the directory that belongs to the specific user.
        dlMSG         : Edit Message progress bar
        text          : Edit Message Content [progress]
        callbackQuery : CallbackQuery

    return:
        "finished"    : Return finished when the request is successful
        "finished"    : Return finished when the request is successful
    """
    try:
        cancel = await util.createBUTTON(btn=text["_cancelCB"])
        canceled = await util.createBUTTON(btn=text["_canceledCB"])
        completed = await util.createBUTTON(btn=text["_completed"])

        with fitz.open(input_file) as doc:
            if doc.page_count >= 3:
                await dlMSG.pin(disable_notification=True, both_sides=True)
            for page in doc:
                pageNo = int(str(page).split(" ")[1]) + 1
                pdfText = page.get_text()
                if 1 <= len(pdfText) <= 1000:
                    try:
                        await callbackQuery.message.reply(
                            f"```🅿🅰🅶🅴 : {pageNo}\n\n{pdfText}```\n@ilovepdf_bot",
                            quote=pageNo == 1,
                        )
                    except FloodWait as e:
                        await asyncio.sleep(e.value + 1)
                        await callbackQuery.message.reply(f"{pdfText}", quote=False)
                elif 1000 <= len(pdfText):
                    slice = [
                        pdfText[i : i + 1000] for i in range(0, len(pdfText), 1000)
                    ]
                    for i, j in enumerate(slice, start=1):
                        try:
                            await callbackQuery.message.reply(
                                f"```🅿🅰🅶🅴 : {pageNo}-{i}\n\n{j}```\n\n@ilovepdf_bot",
                                quote=pageNo == 1,
                            )
                        except FloodWait as e:
                            await asyncio.sleep(e.value + 1)
                            await callbackQuery.message.reply(f"{pdfText}", quote=False)
                if await work.work(callbackQuery, "check", False):
                    try:
                        await dlMSG.edit(
                            text["_upload"].format(pageNo, doc.page_count),
                            reply_markup=cancel,
                        )
                    except Exception:
                        pass
            await dlMSG.edit(text=text["finished"], reply_markup=completed)
        return "finished", "finished"

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
