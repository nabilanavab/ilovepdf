# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/textToPdf/__init__.py"

__author__ = "nabilanavab"
__email__ = "nabilanavab@gmail.com"
__telegram__ = "telegram.dog/nabilanavab"
__copyright__ = "Copyright 2021, nabilanavab"

import os, asyncio, time
from logger import logger
import shutil, sys, math, re
from pyrogram import Client as ILovePDF, filters

iLovePDF = '''
  _   _                  ___  ___  ____ ™
 | | | |   _____ _____  | _ \|   \|  __| 
 | | | |__/ _ \ V / -_) |  _/| |) |  _|  
 |_| |___,\___/\_/\___| |_|  |___/|_|    
                         ❤ [Nabil A Navab] 
                         ❤ Email: nabilanavab@gmail.com
                         ❤ Telegram: @nabilanavab
'''

TXT = {}

SCALE = { 1: "Landscape", 2: "Portrait" }

# FONT PREVIEW: https://graph.org/Nabil-A-Navab-06-15
FONT = {
    1: f"{path}/FONT_LIBRARY/DejaVuSans.ttf",
    2: f"{path}/FONT_LIBRARY/WinterSong-owRGB.ttf",
    3: f"{path}/FONT_LIBRARY/Conquest-8MxyM.ttf",
    4: f"{path}/FONT_LIBRARY/Branda-yolq.ttf",
    5: f"{path}/FONT_LIBRARY/ArianaVioleta-dz2K.ttf",
    6: f"{path}/FONT_LIBRARY/3Dumb.ttf",
    7: f"{path}/FONT_LIBRARY/AlexBrush-Regular.ttf",
    8: f"{path}/FONT_LIBRARY/Archistico_Bold.ttf",
    9: f"{path}/FONT_LIBRARY/Archistico_Simple.ttf",
    10: f"{path}/FONT_LIBRARY/Calligraffiti.ttf",
    11: f"{path}/FONT_LIBRARY/DancingScript-Regular.otf",
    12: f"{path}/FONT_LIBRARY/FFF_Tusj.ttf",
    13: f"{path}/FONT_LIBRARY/GreatVibes-Regular.otf",
    14: f"{path}/FONT_LIBRARY/Kristi.ttf",
    15: f"{path}/FONT_LIBRARY/Pacifico.ttf",
}

COLOR = {
    1: {"color": "black", "code": (0, 0, 0)},
    2: {"color": "grey", "code": (128, 128, 128)},
    3: {"color": "white", "code": (255, 255, 255)},
    4: {"color": "red", "code": (255, 0, 0)},
    5: {"color": "green", "code": (0, 255, 0)},
    6: {"color": "blue", "code": (0, 0, 255)},
}

BACKGROUND_L = {
    1: {"isColor": True, "code": (255, 255, 255), "position": ["w", 20, "w", 10]},
    2: {
        "isColor": False,
        "code": f"{path}/IMAGES/black.png",
        "position": ["w", 20, "w", 10],
    },
    3: {"isColor": True, "code": (128, 128, 128), "position": ["w", 20, "w", 10]},
    4: {
        "isColor": False,
        "code": f"{path}/IMAGES/sanscrit.png",
        "position": ["w", 20, "w", 10],
    },
    5: {
        "isColor": False,
        "code": f"{path}/IMAGES/folded.png",
        "position": ["w", 20, "w", 10],
    },
}

BACKGROUND_P = {
    1: {"isColor": True, "code": (255, 255, 255), "position": ["w", 20, "w", 10]},
    2: {
        "isColor": False,
        "code": f"{path}/IMAGES/black.png",
        "position": ["w", 20, "w", 10],
    },
    3: {"isColor": True, "code": (128, 128, 128), "position": ["w", 20, "w", 10]},
    4: {
        "isColor": False,
        "code": f"{path}/IMAGES/sanscrit.png",
        "position": ["w", 20, "w", 10],
    },
    5: {
        "isColor": False,
        "code": f"{path}/IMAGES/folded.png",
        "position": ["w", 20, "w", 10],
    },
}

_all__ = [
    'TXT',
    'SCALE',
    'FONT',
    'COLOR',
    'BACKGROUND_L',
    'BACKGROUND_P',
]

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
