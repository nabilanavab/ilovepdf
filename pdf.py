#copyright ©️ 2021 nabilanavab
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import telebot
from telebot import types
from PIL import Image
import shutil
from time import sleep

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")

@bot.message_handler(commands=["start"])
def strt(message):
	bot.send_chat_action(message.chat.id, "typing")
	strtMsg = f"Hey [{message.from_user.first_name}](tg://user?id={message.chat.id})..!!This bot will helps you to generate pdf from your images (renaming supported 🥳)\n\nSend me JPG photos as Telegram media.🙂\n\nWhen you are finished; use /generate to create pdf..😉"
	key = types.InlineKeyboardMarkup()
	key.add(types.InlineKeyboardButton("About Dev ❤️", callback_data="strtDevEdt"),types.InlineKeyboardButton("rename PDF 😇", callback_data="strtRnmPdf"))
	bot.send_message(message.chat.id, strtMsg, reply_markup=key)
		
@bot.callback_query_handler(func=lambda call: call.data)
def strtMsgEdt(call):
	edit = call.data
	if edit == 'strtDevEdt':
		aboutDev = f'About Dev. \n\nOwNeR By: @nabiIanavab 😜\nUpdate Channel: @nabiIanavab 😇\n\nSource Code: https://github.com/nabilanavab/ilovepdf\n\nJoin @nabiIanavab , if you ❤ this bot. 😃'
		key = types.InlineKeyboardMarkup()
		key.add(types.InlineKeyboardButton("Back 🔙", callback_data="back"))
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = aboutDev, reply_markup=key)
	elif edit == 'strtRnmPdf':
		hlpMsg = f"When you finished sending images use:\n🤞 /generate - to get your pdf\n\n/start - check whether bot alive\n/help - for more help\n/id - to get your Telegram id\n/generate - Generate pdf frm img's\n/cancel - Delete's your current Queue\n \n`By default your name will be treated as pdf name\nCheck the below image to rename 👇`[­](https://telegra.ph/file/f4f1f656abe32a39cf848.jpg)"
		key = types.InlineKeyboardMarkup()
		key.add(types.InlineKeyboardButton("Back 🔙", callback_data="back"))
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = hlpMsg, reply_markup=key)
	elif edit == 'back':
		strtMsg = f"Hey ..!!This bot will helps you to generate pdf from your images (renaming supported 🥳)\n\nSend me JPG photos as Telegram media.🙂\n\nWhen you finished sending images use:\n/generate to create pdf..😉"
		key = types.InlineKeyboardMarkup()
		key.add(types.InlineKeyboardButton("About Dev ❤️", callback_data="strtDevEdt"),types.InlineKeyboardButton("rename PDF 😇", callback_data="strtRnmPdf"))
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = strtMsg, reply_markup=key)
	
@bot.message_handler(commands=["id"])
def UsrId(message):
	bot.send_chat_action(message.chat.id, "typing")
	bot.send_message(message.chat.id, f'Your ID - `{message.chat.id}`')

@bot.message_handler(commands=["help"])
def hlp(message):
	bot.send_chat_action(message.chat.id, "typing")
	hlpMsg = f"When you finished sending images use:\n🤞 /generate - to get your pdf\n\n/start - check whether bot alive\n/help - for more help\n/id - to get your Telegram id\n/generate - Generate pdf frm img's\n/cancel - Delete's your current Queue\n \n`By default your name will be treated as pdf name\nCheck the below image to rename 👇`[­](https://telegra.ph/file/f4f1f656abe32a39cf848.jpg)"
	bot.send_message(message.chat.id, hlpMsg)
	
PDF = {}
	
@bot.message_handler(content_types=['photo'])
def pic(message):
	picMsgId = bot.reply_to(message, "`Downloading your Image..⏳`",)
	
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
	bot.edit_message_text(chat_id= message.chat.id, text = f"`Added {len(PDF[message.chat.id])} page/'s to your pdf..`🤓\n\n/generate to generate PDF 🤞", message_id = picMsgId.message_id)
	
@bot.message_handler(commands=["cancel"])
def delQueue(message):
	try:
		shutil.rmtree(f'./{message.chat.id}')
		del PDF[message.chat.id]
	except:
	  pass
	finally:
		bot.reply_to(message, "`Queue deleted Successfully..`")

@bot.message_handler(commands=["generate"])
def generate(message):
	newName = message.text.replace('/generate', '')
	images = PDF.get(message.chat.id)
	if isinstance(images, list):
		pgnmbr = len(PDF[message.chat.id])
		del PDF[message.chat.id]
	if not images:
		ntFnded = bot.reply_to(message, "`No image founded.!!👊`")
		bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
		sleep(2)
		bot.delete_message(chat_id = message.chat.id, message_id = ntFnded.message_id)
		return
	gnrtMsgId = bot.send_message(message.chat.id, f'`Generating pdf..💚`')
	if newName == f" id":
		fileName = f"{message.chat.id}" + ".pdf"
	elif len(newName) > 0 and len(newName) <= 25:
		fileName = f"{newName}" + ".pdf"
	elif len(newName) > 25:
		fileName = f"{message.chat.id}" + ".pdf"
	else:
		fileName = f"{message.from_user.first_name}" + ".pdf"
	path = os.path.join(f'./{message.chat.id}', fileName)
	images[0].save(path, save_all=True, append_images=images[1:])
	bot.edit_message_text(chat_id= message.chat.id, text = f'`Uploading pdf...❤️`', message_id = gnrtMsgId.message_id)
	sendfile = open(path,'rb')
	bot.send_document(message.chat.id, sendfile, caption = f'file Name: `{fileName}`\n\n`Total pg\'s: {pgnmbr}`')
	shutil.rmtree(f'./{message.chat.id}')
	bot.edit_message_text(chat_id= message.chat.id, text = f'`Successfully Uploaded 🤫`', message_id = gnrtMsgId.message_id)
	
@bot.message_handler(content_types=['text', 'audio', 'document','gif', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def unsuprtd(message):
	bot.send_chat_action(message.chat.id, "typing")
	unSuprtd = bot.send_message(message.chat.id, f'`unsupported file.. please send me an image..😬`')
	sleep(2)
	bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
	bot.delete_message(chat_id = message.chat.id, message_id = unSuprtd.message_id)
	
bot.polling()
