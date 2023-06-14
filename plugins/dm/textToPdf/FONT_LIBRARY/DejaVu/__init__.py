
import os

async def add_DejaVu(pdf):
    for file_name in os.listdir('./'):
        if file_name.endswith('.ttf'):
            font_path = os.path.join(font_directory, file_name)
            pdf.add_font("DejaVu", '', font_path, uni=True)
