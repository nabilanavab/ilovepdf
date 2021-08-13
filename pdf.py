#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import telebot
from telebot import types
from PIL import Image
import shutil

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start"])
def strt(message):
	bot.send_chat_action(message.chat.id, "typing")
	strtMsg = f"Hey [{message.from_user.first_name}](tg://user?id={message.chat.id})..!!This bot will helps you to generate pdf from your images (renaming supported 🥳)\n\nSend me JPG photos as Telegram media.🙂\n\nWhen you are finished; use /generate to create pdf..😉"
	key = types.InlineKeyboardMarkup()
	key.add(types.InlineKeyboardButton("About Dev ❤️", callback_data="strtDevEdt"),types.InlineKeyboardButton("Help 🙄", callback_data="strtHlpEdt"))
	bot.send_message(message.chat.id, strtMsg, reply_markup=key, parse_mode="Markdown")
		
@bot.callback_query_handler(func=lambda call: call.data)
def strtMsgEdt(call):
	edit = call.data
	if edit == 'strtDevEdt':
		aboutDev = f'About Dev. \n\nOwNeR By: @nabiIanavab 😜\nUpdate Channel: @nabiIanavab 😇\n\nSource Code: https://github.com/nabilanavab/ilovepdf\n\nJoin @nabiIanavab , if you ❤ this bot. 😃'
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = aboutDev)
	elif edit == 'strtHlpEdt':
		hlpMsg = f'When you finished sending images use:\n\n🤞 /generate - to get your pdf (By Default: Your pdf name = your Telegram Id) : to find your id hit 👉 /id \n\n🤞 If you want to rename your pdf file..\nSend 👉 /generate fileName\nEg: /generate @nabilanavab✓\n\n🤞To delete your current Queue use:\n👉 /cancel (delete\'s all images from server..🙊)\n\n\nAll the images send to this bot will be sequentially ordered in the generated PDF 😉\n\nSend me an image to get start..😅'
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = hlpMsg)
		
@bot.message_handler(commands=["id"])
def UsrId(message):
	bot.send_chat_action(message.chat.id, "typing")
	bot.send_message(message.chat.id, f'Your ID - `{message.chat.id}`\n\nYour default pdf name - `{message.chat.id}.pdf`😆', parse_mode="Markdown")

@bot.message_handler(commands=["help"])
def hlp(message):
	bot.send_chat_action(message.chat.id, "typing")
	hlpMsg = f'When you finished sending images use:\n\n🤞 /generate - to get your pdf (By Default: Your pdf name = your Telegram Id) : to find your id hit 👉 /id \n\n🤞 If you want to rename your pdf file..\nSend 👉 /generate fileName\nEg: /generate @nabilanavab✓\n\n🤞To delete your current Queue use:\n👉 /cancel (delete\'s all images from server..🙊)\n\n\nAll the images send to this bot will be sequentially ordered in the generated PDF 😉\n\nSend me an image to get start..😅'
	bot.send_message(message.chat.id, hlpMsg)
	
@bot.message_handler(content_types=['document', 'audio'])
def unsuprtd(message):
	bot.send_chat_action(message.chat.id, "typing")
	bot.reply_to(message, f'`unsupported file.. please send me an image 😒`')
	
PDF = {}
	
@bot.message_handler(content_types=['photo'])
def pic(message):
	picMsgId = bot.reply_to(message, "`Downloading your Image..⏳`", parse_mode="Markdown")
	
	if not isinstance(PDF.get(message.chat.id), list):
		PDF[message.chat.id] = []
	file_info = bot.get_file(message.photo[-1].file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	
	try:
		os.makedirs(f'./{message.chat.id}/imgs')
	except:
		pass
	with open(f'./{message.chat.id}/imgs/{message.chat.id}.jpg', 'wb') as new_file:
		new_file.write(downloaded_file)
	img = Image.open(f'./{message.chat.id}/imgs/{message.chat.id}.jpg').convert("RGB")
	PDF[message.chat.id].append(img)
	bot.edit_message_text(chat_id= message.chat.id, text = f'Total pages: {len(PDF[message.chat.id])} \nDownloading completed..\n/generate - to generate the bot', message_id = picMsgId.message_id)
	
@bot.message_handler(commands=["cancel"])
def delQueue(message):
	try:
		shutil.rmtree(f'./{message.chat.id}')
		del PDF[message.chat.id]
	except:
	  pass
	finally:
		bot.reply_to(message, "`Queue deleted Successfully..`", parse_mode="Markdown")

@bot.message_handler(commands=["generate"])
def generate(message):
	newName = message.text.replace('/generate', '')
	images = PDF.get(message.chat.id)
	if isinstance(images, list):
		del PDF[message.chat.id]
	if not images:
		bot.reply_to(message, "No image founded.!!👊 \n\nplease send me atleast one image🙄 ")
		return
	gnrtMsgId = bot.send_message(message.chat.id, f'`Generating PDF..🤫`', parse_mode="Markdown")
	if len(newName) > 0 and len(newName) <= 25:
		fileName = f"{newName}" + ".pdf"
	elif len(newName) > 25:
		fileName = f"{message.from_user.first_name}" + ".pdf"
	else:
		fileName = f"{message.chat.id}" + ".pdf"
	path = os.path.join(f'./{message.chat.id}', fileName)
	images[0].save(path, save_all=True, append_images=images[1:])
	bot.send_document(message.chat.id, open(path, 'rb'), caption = f"[{message.from_user.first_name}](tg://user?id={msg.from_user.id}) your pDf😉", parse_mode="Markdown")
	shutil.rmtree(f'./{message.chat.id}')
	bot.edit_message_text(chat_id= message.chat.id, text = f'`Successfully Uploaded 🤫`', message_id = gnrtMsgId.message_id)
	
bot.polling()
