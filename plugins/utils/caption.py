# fileName : plugins/utils/caption.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/utils/fncta.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

from plugins.utils    import util
from configs.config   import settings

async def caption(
    data: str, lang_code :str = settings.DEFAULT_LANG,
    password: list = None
) -> str:
    try:
        """ return caption deepending upon the work """"
        
        if data == "encrypt":
            caption = "common['encrypt_caption']".format(password)
        
        caption, _ = await util.translate(text = caption, lang_code = lang_code)
        
        return caption
    
    except Exception as Error:
        logger.exception("🐞 %s : %s" %(file_name, Error))
        return ""

# Author: @nabilanavab
