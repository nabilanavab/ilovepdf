# fileName : plugins/utils/caption.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/utils/fncta.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger           import logger

from plugins.utils    import util
from configs.config   import settings

async def caption(
    data: str,
    args: list = None,
    lang_code :str = settings.DEFAULT_LANG
) -> str:
    try:
        """ return caption deepending upon the work """
        
        if data == "encrypt":
            _, __ = await util.translate(text = "common['encrypt_caption']", lang_code = lang_code)
            caption = _.format(*args)
        elif data == "rename":
            _, __ = await util.translate(text = "common['rename_caption']", lang_code = lang_code)
        else:
            caption = ""
        
        return caption
    
    except Exception as Error:
        logger.exception("🐞 %s : %s" %(file_name, Error))
        return ""

# Author: @nabilanavab
