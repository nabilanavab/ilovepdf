file_name = "plugins/dm/textToPdf/__init__.py"
author_name = "telegram.dog/nabilanavab"
source_code = "https://github.com/nabilanavab/ilovepdf"

path = "plugins/dm/textToPdf/FONT_LIBRARY"

# GLOBAL VARIABLES
# Just a DB Variable
TXT = {}

SCALE = {
        1 : "Landscape",
        2 : "Portrait"
    }

# FONT PREVIEW: https://graph.org/Nabil-A-Navab-06-15
FONT = {
        1 : f"{path}/DejaVuSans.ttf",
        2 : f"{path}/WinterSong-owRGB.ttf",
        3 : f"{path}/Conquest-8MxyM.ttf" },
        4 : f"{path}/Branda-yolq.ttf" },
        5 : f"{path}/ArianaVioleta-dz2K.ttf" },
        6 : f"{path}/3Dumb.ttf" },
        7 : f"{path}/AlexBrush-Regular.ttf" },
        8 : f"{path}/Archistico_Bold.ttf" },
        9 : f"{path}/Archistico_Simple.ttf" },
        10 : f"{path}/Calligraffiti.ttf" },
        11 : f"{path}/DancingScript-Regular.otf" },
        12 : f"{path}/FFF_Tusj.ttf" },
        13 : f"{path}/GreatVibes-Regular.otf" },
        14 : f"{path}/Kristi.ttf" },
        15 : f"{path}/Pacifico.ttf" },
    }

COLOR = {
        1 : { "color" : "white", "code" : (255, 255, 255) },
        2 : { "color" : "black", "code" : (0, 0, 0) },
        3 : { "color" : "grey", "code" : (128, 128, 128) },
        4 : { "color" : "red", "code" : (255, 0, 0) },
        5 : { "color" : "green", "code" : (0, 255, 0) },
        6 : { "color" : "blue", "code" : (0, 0, 255) }
}

BACKGROUND_L = {
        1 : { "isColor" : True, "code" : (255, 255, 255) },
        2 : { "isColor" : True, "code" : (0, 0, 0) },
        3 : { "isColor" : True, "code" : (128, 128, 128) },
        4 : { "isColor" : False, "code" : f"{path}/IMAGES/notebook.png" },
        5 : { "isColor" : False, "code" : f"{path}/IMAGES/sanscrit.png" },
        6 : { "isColor" : False, "code" : f"{path}/IMAGES/folded.png" },
        7 : { "isColor" : False, "code" : f"{path}/IMAGES/imageOne.png" },
        8 : { "isColor" : False, "code" : f"{path}/IMAGES/imageTwo.png" },
}

BACKGROUND_P = {
        1 : { "isColor" : True, "code" : (255, 255, 255) },
        2 : { "isColor" : True, "code" : (0, 0, 0) },
        3 : { "isColor" : True, "code" : (128, 128, 128) },
        4 : { "isColor" : False, "code" : f"{path}/IMAGES/notebook.png" },
        5 : { "isColor" : False, "code" : f"{path}/IMAGES/sanscrit.png" },
        6 : { "isColor" : False, "code" : f"{path}/IMAGES/folded.png" },
        7 : { "isColor" : False, "code" : f"{path}/IMAGES/imageOne.png" },
        8 : { "isColor" : False, "code" : f"{path}/IMAGES/imageTwo.png" },
}

# UPDATE CHANNEL: https://telegram.dog/ilovepdf_bot
