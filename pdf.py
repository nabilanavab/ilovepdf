# copyright ©️ 2021 nabilanavab
# !/usr/bin/python
# -*- coding: utf-8 -*-

#packages Used:
# pip install pyTelegramBotAPI
# pip install pillow
# pip install pyMuPdf

import os
import telebot
from telebot import types
from telebot.types import InputMediaPhoto
from PIL import Image
import shutil
from time import sleep
import fitz

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")

@bot.message_handler(commands=["start"])
def strt(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
		strtMsg = f'''Hey [{message.from_user.first_name}](tg://user?id={message.chat.id})..!!This bot will helps you to generate pdf from your images (& vice-versa 🥳)

🤞 Convert Images to pdf:
Just Send me some images(.jpeg, .jpg, .png files Supported)🙂 When you are finished; use /generate to create pdf..😉

🤞 Convert pdf to Images
Just send/forward me a pdf file..😉'''
		key = types.InlineKeyboardMarkup()
		key.add(types.InlineKeyboardButton("About Dev ❤️", callback_data="strtDevEdt"),types.InlineKeyboardButton("Commands 😇", callback_data="strtRnmPdf"))
		key.add(types.InlineKeyboardButton("Img ♻️ Pdf", callback_data="strtPdfToImg"))
		bot.send_message(message.chat.id, strtMsg, reply_markup=key)
	
	except:
		pass
	
@bot.callback_query_handler(func=lambda call: call.data)
def strtMsgEdt(call):
	edit = call.data
	
	if edit == 'strtDevEdt':
		
		try:
			aboutDev = f'''About Dev:

OwNeD By: @nabilanavab 😜
Update Channel: @nabiIanavab 😇

Source Code: https://github.com/nabilanavab/ilovepdf

Join @nabiIanavab , if you ❤ this bot. 😃'''
			key = types.InlineKeyboardMarkup()
			key.add(types.InlineKeyboardButton("Back 🔙", callback_data="back"))
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = aboutDev, reply_markup=key)
		
		except:
			pass
		
	elif edit == 'strtRnmPdf':
		
		try:
			hlpMsg = f'''/start - check whether bot alive
/help - for help message
/id - to get your Telegram id (default pdf name)
/generate - Generate pdf from your img's
/generate `fileName` - to change pdf name
/cancel - Delete's your current Queue

`By default your telegram will be treated as pdf name
Check below image to rename 👇`[­](https://telegra.ph/file/f4f1f656abe32a39cf848.jpg)'''
			key = types.InlineKeyboardMarkup()
			key.add(types.InlineKeyboardButton("Back 🔙", callback_data="back"))
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = hlpMsg, reply_markup=key)
		
		except:
			pass
		
	elif edit == 'strtPdfToImg':
		
		try:
			pdfToImg = f'''➡️ Convert Images to pdf:

When you finished sending images use: /generate - to get your pdf


➡️ Convert Pdf to Images:

Just send/forward me a pdf file. i will convert it to images anfmd send to you 😉'''
			key = types.InlineKeyboardMarkup()
			key.add(types.InlineKeyboardButton("Back 🔙", callback_data="back"))
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = pdfToImg, reply_markup=key)
		
		except:
			pass
		
	elif edit == 'back':
		
		try:
			strtMsg = f'''Hey..!!This bot will helps you to generate pdf from your images (renaming supported 🥳)

Send me JPG photos as Telegram media.🙂

When you finished sending images use:
/generate to create pdf..😉'''
			key = types.InlineKeyboardMarkup()
			key.add(types.InlineKeyboardButton("About Dev ❤️", callback_data="strtDevEdt"),types.InlineKeyboardButton("Commands 😇", callback_data="strtRnmPdf"))
			key.add(types.InlineKeyboardButton("Img ♻️ Pdf", callback_data="strtPdfToImg"))
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = strtMsg, reply_markup=key)
		
		except:
			pass
		
	elif edit == 'close':
		
		try:
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
			
		except:
			pass
		
@bot.message_handler(commands=["id"])
def UsrId(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
		bot.send_message(message.chat.id, f'Your ID - `{message.chat.id}`')
	
	except:
		pass

@bot.message_handler(commands=["help"])
def hlp(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
		hlpMsg = f'''/start - check whether bot alive
/help - for more help
/id - to get your Telegram id
/generate - Generate pdf frm img's
/cancel - Delete's your current Queue

`By default your name will be treated as pdf name
Check below image to rename 👇`[­](https://telegra.ph/file/f4f1f656abe32a39cf848.jpg)'''
		key = types.InlineKeyboardMarkup()
		key.add(types.InlineKeyboardButton("Close ⌛", callback_data="close"))
		bot.send_message(message.chat.id, hlpMsg, reply_markup=key)
	
	except:
		pass

PDF = {}
media = {}

@bot.message_handler(content_types=['photo'])
def pic(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
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
		bot.edit_message_text(chat_id= message.chat.id, text = f'''`Added {len(PDF[message.chat.id])} page/'s to your pdf..`🤓

/generate to generate PDF 🤞''', message_id = picMsgId.message_id)
	
	except:
		pass

@bot.message_handler(content_types=['document'])
def fls(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
		isPdfOrImg = message.document.file_name
		fileSize = message.document.file_size
		
		fileNm, fileExt = os.path.splitext(isPdfOrImg)
		suprtedFile = ['.jpg','.jpeg','.png']
		
		if fileExt in suprtedFile and fileSize <= 10000000:
		
			try:
				picMsgId = bot.reply_to(message, "`Downloading your Image..⏳`",)
				
				if not isinstance(PDF.get(message.chat.id), list):
					PDF[message.chat.id] = []
				
				file_info = bot.get_file(message.document.file_id)
				downloaded_file = bot.download_file(file_info.file_path)
				
				try:
					os.makedirs(f'./{message.chat.id}/imgs')
				
				except:
					pass
				
				with open(f'./{message.chat.id}/imgs/{message.chat.id}{isPdfOrImg}', 'wb') as new_file:
					new_file.write(downloaded_file)
				
				img = Image.open(f'./{message.chat.id}/imgs/{message.chat.id}{isPdfOrImg}').convert("RGB")
				PDF[message.chat.id].append(img)
				bot.edit_message_text(chat_id= message.chat.id, text = f'''`Added {len(PDF[message.chat.id])} page/'s to your pdf..`🤓

/generate to generate PDF 🤞''', message_id = picMsgId.message_id)
				
			except Exception as e:
				
				bot.edit_message_text(chat_id = message.chat.id, text = f'''Something went wrong..😐

`ERROR: {e}`''', message_id = picMsgId.message_id)
				sleep(5)
				bot.delete_message(chat_id = message.chat.id, message_id = picMsgId.message_id)
				bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
			
		elif fileExt.lower() == '.pdf':
			
			try:
				bot.send_chat_action(message.chat.id, "typing")
				pdfMsgId = bot.reply_to(message, "`Downloading your pdf..⏳`",)
				
				file_info = bot.get_file(message.document.file_id)
				downloaded_file = bot.download_file(file_info.file_path)
				
				try:
					os.makedirs(f'./{message.message_id}pdf{message.chat.id}')
					with open(f'./{message.message_id}pdf{message.chat.id}/{message.chat.id}.pdf', 'wb') as new_file:
						new_file.write(downloaded_file)
				
				except:
					pass
				
				doc = fitz.open(f'./{message.message_id}pdf{message.chat.id}/{message.chat.id}.pdf')
				zoom = 1
				mat = fitz.Matrix(zoom, zoom)
				noOfPages = doc.pageCount
				
				bot.edit_message_text(chat_id = message.chat.id, text = f'`Total pages: {noOfPages}`', message_id = pdfMsgId.message_id)
				
				for pageNo in range(noOfPages):
					
					page = doc.loadPage(pageNo)
					pix = page.getPixmap(matrix = mat)
					cnvrtpg = pageNo + 1
					bot.edit_message_text(chat_id = message.chat.id, text = f'`Converted: {cnvrtpg}/{noOfPages} pgs`', message_id = pdfMsgId.message_id)
					
					with open(f'./{message.message_id}pdf{message.chat.id}/{pageNo}.jpg','wb') as f:
						pix.writePNG(f'./{message.message_id}pdf{message.chat.id}/{pageNo}.jpg')
				
				os.remove(f'./{message.message_id}pdf{message.chat.id}/{message.chat.id}.pdf')
				#imagRelPth = os.listdir(f'./{message.message_id}pdf{message.chat.id}')
				bot.edit_message_text(chat_id = message.chat.id, text = f'`started Uploading..💜`', message_id = pdfMsgId.message_id)
				percNo = 0
				LrgFileNo = 0
				
				directory = f'./{message.message_id}pdf{message.chat.id}/'
				imag = [os.path.join(directory, file) for file in os.listdir(directory)]
				
				
				#bot.send_message(message.chat.id,f'{imag}')
				
				imag.sort(key=os.path.getctime)
				
				#bot.send_message(message.chat.id,f'{imag}')
				
				#bot.send_message(message.chat.id,f'{imag}')
				for i in range(0, len(imag), 10):
					
					imags = imag[i:i+10]
					media[message.chat.id] = []
					for file in imags:
						
						percNo += 1
						percent = (percNo/noOfPages)*100
						bot.edit_message_text(chat_id = message.chat.id, text = f'`Uploaded: {percent}%`', message_id = pdfMsgId.message_id)
						imagePath = file
						#imagePath = os.path.join(f'./{message.message_id}pdf{message.chat.id}', file)
						
						if os.path.getsize(imagePath) >= 1000000:
							
							LrgFileNo += 1
							picture = Image.open(imagePath)
							CmpImg = f'./{message.message_id}pdf{message.chat.id}/temp{LrgFileNo}.jpeg'
							picture.save(CmpImg, "JPEG", optimize=True, quality=50) 
							
							if os.path.getsize(CmpImg) >= 1000000:
								continue
							
							fi = open(CmpImg, "rb")
							media[message.chat.id].append(InputMediaPhoto (fi))
							
							continue
						
						fi = open(imagePath, "rb")
						media[message.chat.id].append(InputMediaPhoto (fi))
						
					bot.send_chat_action(message.chat.id, "upload_photo")
					bot.send_media_group(message.chat.id, media[message.chat.id])
					del media[message.chat.id]
				
				bot.edit_message_text(chat_id = message.chat.id, text = f'`Uploading Completed.. 💛`', message_id = pdfMsgId.message_id)
				shutil.rmtree(f'./{message.message_id}pdf{message.chat.id}')
				
			except Exception as e:
				bot.edit_message_text(chat_id = message.chat.id, text = f'''Something went wrong..😐

`ERROR: {e}`''', message_id = pdfMsgId.message_id)
			
				try:
					shutil.rmtree(f'./{message.message_id}pdf{message.chat.id}')
				
				except:
					pass
				
				sleep(15)
				bot.delete_message(chat_id = message.chat.id, message_id = pdfMsgId.message_id)
				bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
		
		else:
			
			try:
				bot.send_chat_action(message.chat.id, "typing")
				unSuprtd = bot.send_message(message.chat.id, f'`Unsupported file.. please send me an image..`👊')
				sleep(5)
				bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
				bot.delete_message(chat_id = message.chat.id, message_id = unSuprtd.message_id)
			
			except:
				pass
			
	except:
		pass
	
@bot.message_handler(commands=["cancel"])
def delQueue(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
		shutil.rmtree(f'./{message.chat.id}')
		del PDF[message.chat.id]
	
	except:
	  pass
	
	finally:
		bot.reply_to(message, "`Queue deleted Successfully..`")

@bot.message_handler(commands=["generate"])
def generate(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
		newName = message.text.replace('/generate', '')
		images = PDF.get(message.chat.id)
		
		if isinstance(images, list):
			pgnmbr = len(PDF[message.chat.id])
			del PDF[message.chat.id]
		
		if not images:
			ntFnded = bot.reply_to(message, "`No image founded.!!👊`")
			sleep(5)
			bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
			bot.delete_message(chat_id = message.chat.id, message_id = ntFnded.message_id)
			return
		
		gnrtMsgId = bot.send_message(message.chat.id, f'`Generating pdf..💚`')
		
		if newName == f" name":
			fileName = f"{message.from_user.first_name}" + ".pdf"
		
		elif len(newName) > 0 and len(newName) <= 10:
			fileName = f"{newName}" + ".pdf"
		
		elif len(newName) > 10:
			fileName = f"{message.from_user.first_name}" + ".pdf"
		
		else:
			fileName = f"{message.chat.id}" + ".pdf"
		
		path = os.path.join(f'./{message.chat.id}', fileName)
		images[0].save(path, save_all=True, append_images=images[1:])
		bot.edit_message_text(chat_id= message.chat.id, text = f'`Uploading pdf...❤️`', message_id = gnrtMsgId.message_id)
		sendfile = open(path,'rb')
		bot.send_chat_action(message.chat.id, "upload_document")
		bot.send_document(message.chat.id, sendfile, caption = f'file Name: `{fileName}`\n\n`Total pg\'s: {pgnmbr}`')
		shutil.rmtree(f'./{message.chat.id}')
		bot.edit_message_text(chat_id= message.chat.id, text = f'`Successfully Uploaded 🤫`', message_id = gnrtMsgId.message_id)
	
	except:
		pass
	
@bot.message_handler(content_types=['text', 'audio', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def unSuprtd(message):
	
	try:
		bot.send_chat_action(message.chat.id, "typing")
		unSuprtd = bot.send_message(message.chat.id, f'`unsupported file.. please send me an image..😬`')
		sleep(5)
		bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
		bot.delete_message(chat_id = message.chat.id, message_id = unSuprtd.message_id)
	
	except:
		pass
	
bot.polling()
