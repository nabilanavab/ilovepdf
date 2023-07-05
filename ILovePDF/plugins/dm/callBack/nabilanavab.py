# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

from plugins.utils import *

@ILovePDF.on_callback_query(filters.regex("^nabilanavab"))
async def __index__(bot, callbackQuery):
    try:
        data = callbackQuery.data.split("|", 1)[1]  # "nabilanavab|"
        lang_code = await util.getLang(callbackQuery.message.chat.id)

        if data.startswith("aio"):
            text, _ = await util.translate(text=f"_CLICK_RIGHT", lang_code=lang_code)
        else:
            text, _ = await util.translate(text=f"HELP['{data}']", lang_code=lang_code)

        await callbackQuery.answer(text, show_alert=True)

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        await work.work(callbackQuery, "delete", False)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
