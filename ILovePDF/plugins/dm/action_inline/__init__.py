# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

__author__ = "nabilanavab"
__email__ = "nabilanavab@gmail.com"
__telegram__ = "telegram.dog/nabilanavab"
__copyright__ = "Copyright 2021, nabilanavab"

iLovePDF = '''
  _   _                  ___  ___  ____ ™
 | | | |   _____ _____  | _ \|   \|  __| 
 | | | |__/ _ \ V / -_) |  _/| |) |  _|  
 |_| |___,\___/\_/\___| |_|  |___/|_|    
                         ❤ [Nabil A Navab] 
                         ❤ Email: nabilanavab@gmail.com
                         ❤ Telegram: @nabilanavab
'''

from typing import Union
from lang import langList
from configs.log import log
from configs.db import myID
from libgenesis import Libgen
from configs.config import images
from plugins.utils.work import work
from pyrogram import filters, errors
from plugins.utils.util import getLang, translate
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

DATA = {
    'user_id' : { 'id' : 'data' },
}

__all__ = [
    'log',
    'myID',
    'DATA',
    'work',
    'Union',
    'errors',
    'images',
    'Libgen',
    'filters',
    'getLang',
    'langList',
    'translate',
    'InlineKeyboardButton',
    'InlineKeyboardMarkup',
]

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
