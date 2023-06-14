
import os

async def add_DejaVu(pdf):
    for file_name in os.listdir('./'):
        if file_name.endswith('.ttf'):
            font_name = os.path.splitext(file_name)[0]
            font_path = os.path.join(font_directory, file_name)
            pdf.add_font(font_name, '', font_path, uni=True)
