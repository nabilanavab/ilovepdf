# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab


file_name = "ILovePDF/plugins/utils/util.py"

from plugins import *
from configs.db import myID
from itertools import islice
from configs.db import dataBASE
from configs.config import settings
from lang import __users__, langList
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# loading languages
try:
    # Check if multi-language support is enabled
    if settings.MULTI_LANG_SUP:
        # List all files in the 'lang' directory
        langs: list = os.listdir(f"./lang")

        for lang in langs:
            # Filter for Python files, excluding specific init and demo files

            if lang.endswith(".py") and lang not in [
                "__init__.py",
                "__users__.py",
                "__demo__.py",
            ]:
                # Dynamically import the language module
                exec(f"from lang import {lang[:-3]}")
                logger.debug(f"adding {lang[:-3]}")

    else:
        # If multi-language support is not enabled, import the default language
        exec(f"from lang import {settings.DEFAULT_LANG}")
        exec(f"from lang import eng")

except Exception as Error:
    # Log any exceptions that occur during language loading
    logger.debug(f"lang: %s" % (Error), exc_info = True)
    logger.debug(f"ERROR IN DEFAULT LANG: {Error}")


# Button creator for generating inline keyboard buttons
deBUTTON_SPLIT = 2  # Default number of buttons per row
async def createBUTTON(btn: dict, order: int = deBUTTON_SPLIT) -> dict:
    try:
        # https://favtutor.com/blogs/string-to-dict-python
        # btn =  ast.literal_eval(btn)   # convert str to dict

        # Initialize an empty list to hold button objects
        button = []

        # Iterate through the dictionary of buttons
        for key, value in btn.items():

            # Check if the value is a URL
            if value.startswith(tuple(["https://", "http://"])):
                 # Create a button that opens a URL, formatting with the bot's username if necessary
                temp = InlineKeyboardButton(
                    key, url=value.format(myID[0].username)
                )  # add bot_username for creating add grup link else pass

            else:
                # Create a button that triggers a callback
                temp = InlineKeyboardButton(key, callback_data = value)
                # Add the created button to the list
            button.append(temp)
        
        # Organize buttons into rows based on the specified order
        if order == deBUTTON_SPLIT:
            # Split the buttons into rows of the default size
            keyboard = [
                button[i : i + deBUTTON_SPLIT]
                for i in range(0, len(button), deBUTTON_SPLIT)
            ]

        else:
            # Create a list of integers for the new order
            new_order = [int(x) for x in str(order)]
            button = iter(button)
            # Create rows based on the specified custom sizes
            keyboard = [list(islice(button, elem)) for elem in new_order]
        
        # Return the constructed inline keyboard markup
        return InlineKeyboardMarkup(keyboard)
    
    except Exception as Error:
        # Log any exceptions that occur during button creation
        logger.exception("🐞 %s : %s" % (file_name, Error))


#  TEXT, BUTTON TRANSLATOR 
async def translate(
    text :str = None,
    button :dict = None,
    asString :bool = False,
    order :int = deBUTTON_SPLIT,
    lang_code :str = settings.DEFAULT_LANG,
) -> dict:
    rtn_text: int = text
    rtn_button: dict = button
    try:
        # Translate the provided text if it's not None
        if text is not None:
            # Dynamic language evaluation
            rtn_text = eval(f"{lang_code}.{text}")

        # Translate the provided button if it's not None
        if button is not None:
            rtn_button = eval(f"{lang_code}.{button}")

    except Exception as Error:
        # Log error if translation fails and fallback to English
        logger.debug(f"❌❌ can't find {text} : %s" % (Error))
        if text is not None:
            rtn_text = eval(f"eng.{text}")
        if button is not None:
            rtn_button = eval(f"eng.{button}")

    finally:
        # Return translated text and button if asString is True
        if asString:
            return rtn_text, rtn_button  # return button as String
    
    try:
        # Create button markup if a button dictionary is provided
        if button is not None:
            rtn_button = await createBUTTON(btn = rtn_button, order = order)

    except Exception as Error:
        logger.debug("🚫 %s: %s" % (file_name, Error))

    finally:
        return (
            rtn_text,
            rtn_button,
        )  # return desired text, button (one text+button at once)


#  GET USER LANG CODE 
async def getLang(chatID: int) -> str:

    if not settings.MULTI_LANG_SUP:      # if multiple lang not supported
        return str(settings.DEFAULT_LANG)           # return default lang
    
    # Retrieve user's language from the user language dictionary
    lang = __users__.userLang.get(
        int(chatID), str(settings.DEFAULT_LANG)
    )  # else return corresponding lang code

    return (
        lang if lang in langList else settings.DEFAULT_LANG
    )  # return lang code if in langList(
    # this way you can simply remove lang by removing lang from list)


#  Add values to callback dictionary, potentially modifying existing keys
async def editDICT(
    inDir: dict, value :bool = False, front = False
) -> dict:
    outDir = {}

    if front:  # changes cb in UI
        for i, j in inDir.items():
            outDir[i.format(front)] = j
        inDir = outDir

    if value and type(value) != list:  # changes cb.data
        for i, j in inDir.items():
            outDir[i] = j.format(value)
    
    # If value is a list
    elif value and type(value) == list:

        # If there are two values in the list
        if len(value) == 2:
            for i, j in inDir.items():
                outDir[i] = j.format(value[0], value[1])
        
        # If there are three values in the list
        if len(value) == 3:
            for i, j in inDir.items():
                outDir[i] = j.format(value[0], value[1], value[2])
    
    # Return the modified dictionary
    return outDir


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD