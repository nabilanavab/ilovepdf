# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/file_process/watermark45.py"

import fitz
from logger import logger 


async def add_text_watermark(input_file, output_file, watermark_text):
    try:
        with fitz.open(input_file) as pdf:
            for page in pdf:

                font = fitz.Font(fontname="tiit")
                text_width = font.text_length(
                    watermark_text, fontsize=int(page.bound().height // 20)
                )

                tw = fitz.TextWriter(page.rect, opacity=0.5, color=(0, 0, 0))

                txt_bottom, txt_left = int((page.bound().width - text_width) / 2), int(
                    (page.bound().height - page.bound().height / 20) / 2
                )

                tw.append(
                    (txt_bottom, txt_left),
                    watermark_text,
                    fontsize=int(page.bound().height // 20),
                    font=font,
                )
                tw.write_text(page)

            pdf.save(output_file)
        return True, output_file
    except Exception as Error:
        logger.exception("1️⃣ 🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error


async def watermarkPDF(input_file: str, cDIR: str, watermark) -> (bool, str):
    try:
        output_path = f"{cDIR}/outPut.pdf"

        success, output_file = await add_text_watermark(
            input_file=input_file, output_file=output_path, watermark_text=watermark
        )
        if not success:
            return False, output_file
        return True, output_file
    except Exception as Error:
        logger.exception("2️⃣ 🐞 %s: %s" % (file_name, Error), exc_info=True)
        return False, Error

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
