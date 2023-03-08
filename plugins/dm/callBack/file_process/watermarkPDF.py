# fileName : plugins/dm/callBack/index.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/index.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

async def askWatermark(bot, callbackQuery, question: str, data: str) -> ( bool, list ):
    try:
        while True:
            watermark = await bot.ask(
                chat_id = callbackQuery.from_user.id,
                reply_to_message_id = callbackQuery.message.id,
                text = question, filters = None
            )
            if watermark.text == "/exit":
                return False, input_file
            elif data == "wa|img" and watermark.document:
                if os.path.splitext(watermark.document.file_name)[1].lower() in [".png", ".jpeg", ".jpg"]:
                    return True, [watermark.document.file_size, watermark.document.file_id]
            elif data == "wa|pdf" and watermark.photo:
                if os.path.splitext(watermark.document.file_name)[1].lower() == ".pdf":
                    return True, [watermark.document.file_size, watermark.document.file_id]
            elif data == "wa|txt" and watermark.text:
                return True, watermark.text
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

async def get_color_by_name(COLOR_CODE):
    color_codes = {
        'R': (255, 0, 0),
        'G': (0, 255, 0),
        'N': (0, 0, 255),
        'Y': (255, 255, 0),
        'O': (255, 165, 0),
        'V': (238, 130, 238),
        'C': (165, 62, 62),
        'B': (0, 0, 0),
        'W': (255, 255, 255),
    }
    return color_codes.get(COLOR_CODE, (0, 0, 0))

async def get_position(pg_width, pg_height, text_width, position):
    bottomLeft = {
        "T" : [int((pg_width-text_width)/2), int(pg_height/20)],
        "M" : [int((pg_width-text_width)/2), int((pg_height-pg_height/20)/2)],
        "B" : [int((pg_width-text_width)/2), int(pg_height-pg_height/20)]
    }
    return bottomLeft[position][0], bottomLeft[position][1]

async def add_text_watermark(input_file, output_file, watermark_text, opacity, position, color):
    try:
        COLOR_CODE = await get_color_by_name(color)
        # Open PDF file
        with fitz.open(input_file) as pdf:
            for page in pdf:
                
                font = fitz.Font(fontname="tiit")
                text_width = font.text_length(watermark_text, fontsize=int(page.bound().height//20))
                
                tw = fitz.TextWriter(page.rect, opacity = int(opacity)/10, color = COLOR_CODE)
                txt_bottom, txt_left = await get_position(
                    pg_width=page.bound().width, pg_height=page.bound().height, text_width=text_width, position=position[-1]
                )
                
                tw.append((txt_bottom, txt_left), watermark_text, fontsize = int(page.bound().height//20), font = font)
                tw.write_text(page)
                
            pdf.save(output_file)
        return True, output_file
    except Exception as Error:
        logger.exception("1️⃣ 🐞 %s: %s" %(fileName, Error), exc_info = True)
        return False, Error

async def add_image_watermark(input_file, output_file, watermark, opacity, position):
    try:
        with Image.open(wa_file) as wa:
            if int(data[2][-2:]) != 10:
                data = wa.convert("RGBA").getdata()
                newData = []
                for item in data:
                    if item[0] in range(200, 255) and item[1] in range(200, 255) and item[2] in range(200, 255):
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                wa.putdata(newData)
                wa.save(wa_file, "PNG")
            imgWidth, imgHeight = wa.size
        
        with fitz.open(input_file) as file_handle:
            for page in file_handle:
                r = page.rect
                page.insert_image(
                    fitz.Rect(r.x0/4, 0, (r.x0/4) + imgHeight, imgWidth),
                    stream = open(wa_file, "rb").read()
                )
            file_handle.save(output_pdf)
        return True, output_file
    except Exception as Error:
        logger.exception("2️⃣ 🐞 %s: %s" %(fileName, Error), exc_info = True)
        return False, Error

