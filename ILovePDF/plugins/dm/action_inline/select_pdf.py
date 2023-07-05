# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)

from . import *

@ILovePDF.on_chosen_inline_result()
async def chosen_inline_result(bot, chosen_inline_result):
    try:
        # default search no log
        if not DATA.get(chosen_inline_result.from_user.id, False):
            return

        lang_code = await getLang(chosen_inline_result.from_user.id)
        trCHUNK, _ = await translate(text="INLINE['edit']", lang_code=lang_code)

        data = DATA[chosen_inline_result.from_user.id][
            int(chosen_inline_result.result_id)
        ]
        log_msg = await bot.send_photo(
            chat_id=int(log.LOG_CHANNEL),
            photo=data["thumb"],
            caption=data["caption"]
            + f"\n\nUSER ID: {chosen_inline_result.from_user.id}"
            f"\nView Profile: {chosen_inline_result.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✅ B@N ✅",
                            callback_data=f"banC|{chosen_inline_result.from_user.id}",
                        )
                    ]
                ]
            ),
        )

        if chosen_inline_result.inline_message_id is None:
            return

        await bot.edit_inline_reply_markup(
            inline_message_id=chosen_inline_result.inline_message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=trCHUNK[0],
                            callback_data=f"lib|{log_msg.id}|{chosen_inline_result.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            text=trCHUNK[1],
                            switch_inline_query_current_chat=f"{chosen_inline_result.query}",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=trCHUNK[2],
                            url=f"https://t.me/{myID[0].username}?start=-m{log_msg.id}",
                        )
                    ],
                ]
            ),
        )
        # if inline cache is 0 set below line
        # del DATA[chosen_inline_result.from_user.id]
        return

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (fileName, Error), exc_info=True)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
