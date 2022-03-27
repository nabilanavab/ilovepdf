# !/USR/BIN/PYTHON
# -*- COADING: UTF-8 -*-
# COPYRIGHT ©️ 2021 NABILANAVAB

'''
  _   _                  ___  ___  ____ ™
 | | | |   _____ _____  | _ \|   \|  __| 
 | | | |__/ _ \ V / -_) |  _/| |) |  _|  
 |_| |___,\___/\_/\___| |_|  |___/|_|    
                         [Nabil A Navab] 
                         Email: nabilanavab@gmail.com
                         Telegram: @nabilanavab
 '''

import logging
from pyromod import listen
from Configs.dm import Config
from pyrogram import Client, idle

# LOGGING INFO: DEBUG
logging.basicConfig(
    level = logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# GLOBAL VARIABLES
PDF = {}            # save images for generating pdf
PROCESS = []        # to check current process
invite_link = None

# PLUGIN DIRECTORY
plugin = dict(
    root = "plugins"
)

# PYROGRAM BOT AUTHENTIFICATION
bot = Client(
    "ILovePDF",
    plugins = plugin,
    api_id = Config.API_ID,
    parse_mode = "markdown",
    api_hash = Config.API_HASH,
    bot_token = Config.API_TOKEN
)

bot.start()
idle()
bot.stop()
