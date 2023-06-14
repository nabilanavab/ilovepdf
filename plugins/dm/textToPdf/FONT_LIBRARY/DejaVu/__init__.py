file_name = "plugins/dm/textToPdf/__init__.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

import os
from logger import logger

font_directory = 'plugins/dm/textToPdf/FONT_LIBRARY/DejaVu'

async def add_DejaVu(pdf):
    for file_name in os.listdir(font_directory):
        if file_name.endswith('.ttf'):
            font_path = os.path.join(font_directory, file_name)
            pdf.add_font("DejaVu", '', font_path, uni=True)
    return pdf

# CONTACT AUTHOR : nabilanavab@gmail.com
