# fileName : lang/__init__.py
# copyright ©️ 2021 nabilanavab

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

