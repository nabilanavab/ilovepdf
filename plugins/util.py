# fileName : plugins/util.py
# copyright ©️ 2021 nabilanavab

import os
from logger import logger
from lang import __users__
from itertools import islice
from configs.db import dataBASE
from configs.config import settings
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# loading languages
try:
    if settings.MULTI_LANG_SUP:
        langs = os.listdir(f"./lang")
        for lang in langs:
            if lang.endswith(".py") and lang not in ["__init__.py", "__users__.py", "__demo__.py"]:
                exec(f"from lang import {lang[:-3]}")
    else:
        exec(f"from lang import {settings.DEFAULT_LANG}")
        exec(f"from lang import eng")
except Exception as e:
    logger.debug(f"lang/__init__.py: %s" %(e), exc_info=True)
    try:
        logger.debug(f"Adding Default language {settings.DEFAULT_LANG}")
    except Exception as e:
        logger.debug(f"ERROR IN DEFAULT LANG: {e}")

# ====================================================> BUTTON CREATOR <===============================================================================================
deBUTTON_SPLIT = 2
async def createBUTTON(btn, order=deBUTTON_SPLIT):
    try:
        # https://favtutor.com/blogs/string-to-dict-python
        # btn =  ast.literal_eval(btn)   # convert str to dict
        button = []
        for key, value in btn.items():
            if value.startswith(tuple(["https://", "http://"])):
                temp = InlineKeyboardButton(key, url=value)
            else:
                temp = InlineKeyboardButton(key, callback_data=value)
            button.append(temp)
        if order == deBUTTON_SPLIT:
             keyboard = [button[i: i+deBUTTON_SPLIT] for i in range(0, len(button), deBUTTON_SPLIT)] 
        else:
            new_order = [int(x) for x in str(order)]
            button = iter(button)
            keyboard = [list(islice(button, elem)) for elem in new_order]
        
        return InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logger.debug(f"plugin/util/createBUTTON: %s" %(e), exc_info=True)

# =======================================================================> TEXT, BUTTON TRANSLATOR <===================================================================
async def translate(text=None, button=None, asString=False, order=deBUTTON_SPLIT,  lang_code=settings.DEFAULT_LANG):
    rtn_text = text; rtn_button = button
    try:
        if text is not None:
            rtn_text = eval(f"{lang_code}.{text}")
        if button is not None:
            rtn_button = eval(f"{lang_code}.{button}")
    except Exception as e:
        logger.debug(f"❌❌ can't find {text} : %s" %(e))
        if text is not None:
            rtn_text = eval(f"eng.{text}")
        if button is not None:
            rtn_button = eval(f"eng.{button}")
    finally:
        if asString:
            return rtn_text, rtn_button    # return button as String
    try:
        if button is not None:
            rtn_button = await createBUTTON(btn=rtn_button, order=order)
    except Exception as e:
        logger.debug("🚫 PLUGIN/UTIL/TRANSLATE/CREATE_BUTTON: %s" %(e))
    finally:
        return rtn_text, rtn_button        # return desired text, button (one text+button at once)

# =====================================================================================================================> GET USER LANG CODE <==========================
async def getLang(chatID):
    if not settings.MULTI_LANG_SUP:
        return str(settings.DEFAULT_LANG)
    return __users__.userLang.get(int(chatID), str(settings.DEFAULT_LANG))     # else return corresponding lang code

# =====================================================> ADD VALUES TO CB DICT <=======================================================================================
async def editDICT(inDir:"dict", value=False, front=False) -> "dict":
    outDir = {}
    
    if front:                              # changes cb in UI
        for i, j in inDir.items():
            outDir[i.format(front)] = j
        inDir = outDir
    if value:                              # changes cb.data
        for i, j in inDir.items():
            outDir[i] = j.format(value)
    return outDir

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
