# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/pdf.py"

from configs.config import bot
from telebot import async_telebot


# GLOBAL VARIABLES
PDF = {}  # save images for generating pdf
works = {"u": [], "g": []}  # broken works

pyTgLovePDF = async_telebot.AsyncTeleBot(bot.API_TOKEN, parse_mode="Markdown")
# TELEBOT (pyTelegramBotAPI) Asyncio [for uploading group doc, imgs]

pyTgLovePDF.polling()


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
