# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

from plugins.utils import util
from configs.config import settings


async def caption(
    data: str, args: str = None, lang_code: str = settings.DEFAULT_LANG
) -> str:
    try:
        """return caption deepending upon the work"""

        if data == "encrypt":
            _, __ = await util.translate(
                text="INDEX['encrypt_caption']", lang_code=lang_code
            )
            caption = _.format(*args)
        elif data == "rename":
            _, __ = await util.translate(
                text="INDEX['rename_caption']", lang_code=lang_code
            )
            caption = _.format(*args)
        elif data == "compress":
            _, __ = await util.translate(
                text="INDEX['compress_caption']", lang_code=lang_code
            )
            caption = _.format(*args)
        else:
            caption = ""
        return caption

    except Exception as Error:
        logger.exception("🐞 %s : %s" % (file_name, Error))
        return ""


# Author: @nabilanavab
