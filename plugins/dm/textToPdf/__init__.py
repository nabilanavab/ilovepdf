file_name = "plugins/dm/textToPdf/__init__.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

# GLOBAL VARIABLES

# Just a DB Variable
TXT = {}

SCALE = {
        1 : "Landscape",
        2 : "Portrait"
    }

FONT = {
        1 : { "default" : True, "name" : "Times" },
        2 : { "default" : True, "name" : "Courier" },
        3 : { "default" : True, "name" : "Helvetica" },
        4 : { "default" : True, "name" : "Symbol" },
        5 : { "default" : True, "name" : "ZapfDingbats" }
    }

COLOR = {
        1 : { "color" : "white", "code" : (255, 255, 255) },
        2 : { "color" : "black", "code" : (0, 0, 0) },
        3 : { "color" : "grey", "code" : (128, 128, 128) },
        4 : { "color" : "red", "code" : (255, 0, 0) },
        5 : { "color" : "green", "code" : (0, 255, 0) },
        6 : { "color" : "blue", "code" : (0, 0, 255) }
}

PAGE_SIZE = {}

# UPDATE CHANNEL: https://telegram.dog/ilovepdf_bot
