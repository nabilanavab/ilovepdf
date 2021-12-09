# copyright ©️ 2021 nabilanavab
# fileName: configs.py
# Total time wasted ~ 250 hrs



import os
    
    
    
    
    
# Config Variables
class Config(object):
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    API_TOKEN = os.environ.get("API_TOKEN")
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL")
    CONVERT_API = os.environ.get("CONVERT_API")
    MAX_FILE_SIZE = os.environ.get("MAX_FILE_SIZE")
    OWNER_ID = os.environ.get("OWNER_ID")
    BANNED_USER = os.environ.get("BANNED_USER")
    PDF_THUMBNAIL = "./thumbnail.jpeg"
    
    
    
    
    
# Message Variables
class Msgs(object):
    
    
    welcomeMsg = """Hey [{}](tg://user?id={})..!! This bot will helps you to do many things with pdf's 🥳

Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert PDF to images`
◍ `Convert files to pdf`                                                                         

Update Channel: @ilovepdf_bot 🤩

[Source Code 🏆](https://github.com/nabilanavab/ilovepdf)
[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
    
    
    feedbackMsg = """
[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
    
    
    forceSubMsg = """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only Channel Members Can Use 🚶
    
This Means You Need To Join The Below Mentioned Channel Before Using Me!

hit on "retry ♻️" after joining.. 😅
"""
    
    
    foolRefresh = """I Like your Smartness,

But Don't be Oversmart 🤧
"""
    
    
    fullPdfSplit = """If you want to split a pdf,

you need to send limits too..🙃
"""
    
    
    bigFileUnSupport = """Due to Overload, bot supports only {}mb files

`please Send me a file less than {}mb Size`🙃
"""
    
    
    encryptedFileCaption = """Page Number: {}
key 🔐: `{}`"""
    
    
    imageAdded = """`Added {} page/'s to your pdf..`🤓

/generate to generate PDF 🤞
"""
    
    
    errorEditMsg = """Something went wrong..😐

ERROR: `{}`

For bot updates join @ilovepdf_bot 💎
"""
    
    
    pdfReplyMsg = """`Total pages: {}pgs`

__Unlike all other bots, this bot start sending images without converting the entire PDF to pages__ 😉

reply:
/extract - __to get entire pages__
/extract `pgNo` - __to get a specific page__
/extract `start:end` - __to get all the images b/w__


/encrypt `password` - to set password
/text - to extract text from pdf

Join Update Channel @ilovepdf_bot, More features soon 🔥
"""
    
    
    aboutDev = """About Dev:

OwNeD By: @nabilanavab 😜
Update Channel: @ilovepdf_bot 😇                                                                

Lang Used: Python🐍
[Source Code](https://github.com/nabilanavab/ilovepdf)

Join @ilovepdf_bot, if you ❤ this

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
    
    
    I2PMsg = """Images to pdf :

        Just Send/forward me some images. When you are finished; use /generate to get your pdf..😉

 ◍ Image Sequence will be considered 🤓
 ◍ For better quality pdfs(send images without Compression) 🤧
 
 ◍ `/delete` - Delete's the current Queue 😒
 ◍ `/id` - to get your telegram ID 🤫                                                            
 
 ◍ RENAME YOUR PDF:
 
    - By default, your telegram ID will be treated as your pdf name..🙂
    - `/generate fileName` - to change pdf name to fileName🤞
    - `/generate name` - to get pdf with your telegram name

For bot updates join @ilovepdf_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
    
    
    P2IMsg = """PDF to images:

        Just Send/forward me a pdf file.

 ◍ I will Convert it to images ✌️
 ◍ if Multiple pages in pdf(send as albums) 😌
 ◍ Page numbers are sequentially ordered 😬
 ◍ Send images faster than anyother bots 😋
 ◍ /cancel : to cancel a pdf to image work                                                       

1st bot on telegram wich send images without converting entire pdf to images

For bot updates join @ilovepdf_bot 💎

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
    
    
    F2PMsg = """Files to PDF:

        Just Send/forward me a Supported file.. I will convert it to pdf and send it to you..😎

◍ Supported files(.epub, .xps, .oxps, .cbz, .fb2) 😁
◍ No need to specify your telegram file extension 🙄
◍ Only Images & ASCII characters Supported 😪
◍ added 30+ new file formats that can be converted to pdf..
API LIMITS..😕

For bot updates join @ilovepdf_bot 💎                                                           

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
    
    
    warningMessage = """WARNING MESSAGE ⚠️:

◍ This bot is completely free to use so please dont spam here 🙏

◍ Please don't try to spread 18+ contents 😒

IF THERE IS ANY KIND OF REPORTING, BUGS, REQUESTS, AND SUGGESTIONS PLEASE CONTACT @nabilanavab

For bot updates join @ilovepdf_bot 💎                                                           

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""
    
    
    back2Start = """Hey..!! This bot will helps you to do many things with pdf's 🥳

Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert PDF to images`
◍ `Convert files to pdf`

For bot updates join @ilovepdf_bot 💎                                                           

[Write a feedback 📋](https://t.me/nabilanavabchannel/17?comment=10)
"""

# please don't try to steel this code,
# god will asks you :(
