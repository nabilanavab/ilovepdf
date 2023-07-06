# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/lang/__init__.py"

from configs.config import settings

langList = {
        "eng" : ["🅴🅽🅶🅻🅸🆂🅷", "English"] ,
        "arb" : ["🅰🆁🅰🅱🅸🅲", "عربي"] ,
        "hnd" : ["🅷🅸🅽🅳🅸", "हिन्दी" ] ,
        "uzb" : ["🆄🆉🅱🅴🅺", "Uzbek"] ,
    }

# Display Lang in a Beutiful Way
async def disLang(lang):
    if lang in langList:
        return langList[lang][0]
    else:
        return langList[settings.DEFAULT_LANG][0]

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
