# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/callback.py"

from plugins import *
from lang import langList
from plugins.utils import *
from configs.db import myID
from datetime import datetime
from pyrogram.types import ForceReply
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

imgg = {"img": "I", "doc": "D", "zip": "zip", "tar": "tar"}

annotSet = {
    0: "STAMP_Approved",
    1: "STAMP_AsIs",
    2: "STAMP_Confidential",
    3: "STAMP_Departmental",
    4: "STAMP_Experimental",
    5: "STAMP_Expired",
    6: "STAMP_Final",
    7: "STAMP_ForComment",
    8: "STAMP_ForPublicRelease",
    9: "STAMP_NotApproved",
    10: "STAMP_NotForPublicRelease",
    11: "STAMP_Sold",
    12: "STAMP_TopSecret",
    13: "STAMP_Draft",
}


@ILovePDF.on_callback_query(filters.regex("^pdf"))
async def _pdf(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return

        await callbackQuery.answer()
        data = callbackQuery.data

        if data == "pdf":
            tTXT, tBTN = await util.translate(
                button="PDF_MESSAGE['pdf_button']", order=22222221, lang_code=lang_code
            )
            return await callbackQuery.message.edit_reply_markup(tBTN)

        data = data.split("|", 1)[1]

        if data == "more":
            tTXT, tBTN = await util.translate(
                button="BUTTONS['rotate']", order=1221, lang_code=lang_code
            )
        elif data == "rotate":
            tTXT, tBTN = await util.translate(
                button="BUTTONS['rotate']", order=1221, lang_code=lang_code
            )
        elif data == "txt":
            tTXT, tBTN = await util.translate(
                button="BUTTONS['txt']", order=1221, lang_code=lang_code
            )
        elif data == "format":
            tTXT, tBTN = await util.translate(
                button="BUTTONS['format']", order=112211, lang_code=lang_code
            )
        elif data == "trade":
            tTXT, tBTN = await util.translate(
                button="BUTTONS['trade']", order=121, lang_code=lang_code
            )
        elif data == "filter":
            tTXT, tBTN = await util.translate(
                button="BUTTONS['filter']", order=1221, lang_code=lang_code
            )
        elif data == "T2P":
            tTXT, tBTN = await util.translate(
                button="pdf2TXT['font_btn']", order=12121, lang_code=lang_code
            )

        elif data.startswith("wa"):
            if data == "wa":
                tTXT, tBTN = await util.translate(
                    button="BUTTONS['type']", order=131, lang_code=lang_code
                )
            else:
                typ = data.split("|")[1]
                if "o" not in data:
                    tTXT, tBTN = await util.translate(
                        text="BUTTONS['op']", lang_code=lang_code
                    )
                    tTXT = await util.editDICT(
                        inDir=tTXT, value=typ, front=f"{typ}".upper()
                    )
                    tTXT = await util.createBUTTON(tTXT, "1551")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
                elif "p" not in data:
                    data = data.split("|")[-1]
                    if typ == "txt":
                        tTXT, tBTN = await util.translate(
                            text="BUTTONS['poTXT']", lang_code=lang_code
                        )
                    else:
                        tTXT, tBTN = await util.translate(
                            text="BUTTONS['po']", lang_code=lang_code
                        )
                    tTXT = await util.editDICT(
                        inDir=tTXT, value=[typ, data], front=f"{typ}".upper()
                    )
                    tTXT = await util.createBUTTON(tTXT, "131")
                    return await callbackQuery.message.edit_reply_markup(tTXT)
                else:
                    data, color = data.split("|")[-2:]
                    tTXT, tBTN = await util.translate(
                        text="BUTTONS['color']", lang_code=lang_code
                    )
                    tTXT = await util.editDICT(
                        inDir=tTXT, value=[typ, data, color], front=f"{typ}".upper()
                    )
                    tTXT = await util.createBUTTON(tTXT, "13331")
                    return await callbackQuery.message.edit_reply_markup(tTXT)

        elif data.startswith("img"):
            if data == "img":
                tTXT, tBTN = await util.translate(
                    button="BUTTONS['toImage']", order=1221, lang_code=lang_code
                )
            else:
                data = data.split("|", 1)[1]
                tTXT, tBTN = await util.translate(
                    text="BUTTONS['imgRange']", lang_code=lang_code
                )
                tTXT = await util.editDICT(
                    inDir=tTXT, value=imgg[f"{data}"], front=f"{data}".upper()
                )
                tTXT = await util.createBUTTON(tTXT, "121")
                return await callbackQuery.message.edit_reply_markup(tTXT)

        elif data.startswith("stp"):
            if data == "stp":
                tTXT, tBTN = await util.translate(
                    button="BUTTONS['stamp']", order=1112222221, lang_code=lang_code
                )
            else:
                data = int(data.split("|", 1)[1])
                tTXT, _ = await util.translate(
                    text="BUTTONS['stampA']", lang_code=lang_code
                )
                tTXT = await util.editDICT(
                    inDir=tTXT, value=f"{data}", front=f"{annotSet[data]}".upper()
                )
                tTXT = await util.createBUTTON(tTXT, "122221")
                return await callbackQuery.message.edit_reply_markup(tTXT)

        # edit button
        return await callbackQuery.message.edit_reply_markup(tBTN)
    except Exception as e:
        logger.exception("🐞 %s: %s" % (file_name, e), exc_info=True)


@ILovePDF.on_callback_query(filters.regex("beta"))
async def _beta(bot, callbackQuery):
    try:
        await callbackQuery.answer()

        lang_code = await util.getLang(callbackQuery.message.chat.id)
        tTXT, tBTN = await util.translate(
            text="_BETA_MESSAGE", button="RESTART['btn']", order=1, lang_code=lang_code
        )

        referal_link = (
            f"https://t.me/{myID[0].username}?start=-r{callbackQuery.message.chat.id}"
        )
        return await callbackQuery.message.reply(
            text=tTXT.format(referal_link, f"http://t.me/share/url?url={referal_link}"),
            reply_markup=tBTN,
            disable_web_page_preview=True,
        )
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)


@ILovePDF.on_callback_query(filters.regex("^aio"))
async def _aio(bot, callbackQuery):
    try:
        lang_code = await util.getLang(callbackQuery.message.chat.id)
        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return

        await callbackQuery.answer()
        data = callbackQuery.data

        if data == "aio":
            tTXT, tBTN = await util.translate(
                text="AIO['aio']",
                button="AIO['aio_button']",
                order=121,
                lang_code=lang_code,
            )
            return await callbackQuery.message.edit(
                text=tTXT.format(
                    callbackQuery.message.reply_to_message.document.file_name,
                    await render.gSF(
                        callbackQuery.message.reply_to_message.document.file_size
                    ),
                ),
                reply_markup=tBTN,
            )

        # encrypted/non encrypted input pdf file
        elif data in ["aioInput|enc", "aioInput|dec"]:
            tTXT, tBTN = await util.translate(text="AIO", order=1, lang_code=lang_code)
            if data == "aioInput|enc":
                input_str = await bot.ask(
                    text=tTXT["waitPASS"],
                    chat_id=callbackQuery.from_user.id,
                    reply_to_message_id=callbackQuery.message.id,
                    reply_markup=ForceReply(True, tTXT["waitPASS"]),
                )
                try:
                    await input_str.reply_to_message.delete()
                except:
                    pass
                await input_str.delete()

            aio_list_btn = []
            for index, (key, value) in enumerate(tTXT["out_button"].items()):
                btn = [InlineKeyboardButton(key, value)]
                if index + 1 <= len(tTXT["out_values"]):
                    btn.append(
                        InlineKeyboardButton(
                            tTXT["false"]
                            if tTXT["out_values"][index].endswith("{F}")
                            else tTXT["true"],
                            tTXT["out_values"][index],
                        )
                    )
                else:
                    next_key, next_value = list(tTXT["out_button"].items())[index + 1]
                    btn.append(InlineKeyboardButton(next_key, next_value))
                    aio_list_btn.append(btn)
                    break
                aio_list_btn.append(btn)
            return await callbackQuery.message.edit(
                text=tTXT["passMSG"].format(
                    callbackQuery.message.reply_to_message.document.file_name,  # password 300 char limit
                    await render.gSF(
                        callbackQuery.message.reply_to_message.document.file_size
                    ),
                    input_str.text[:50]
                    if (data == "aioInput|enc" and input_str)
                    else None,
                    None,
                    None,
                    None,
                ),
                reply_markup=InlineKeyboardMarkup(aio_list_btn),
            )

        # data1 = "meta/enc/form/comp/water/n.." , data2 = "{}/True/False"
        data1, data2 = data.split("|")[1:]
        buttons = callbackQuery.message.reply_markup.inline_keyboard
        callback = [
            element.callback_data
            for button in buttons
            for index, element in enumerate(button, start=1)
            if index % 2 == 0
        ]
        all_data = [
            "{F}" if element.endswith("{F}") else element.split("|")[-1]
            for element in callback
        ][:-1]
        dataARRANGEMENT = {
            "met": 0,
            "pre": 1,
            "com": 2,
            "txt": 3,
            "rot": 4,
            "for": 5,
            "enc": 6,
            "wat": 7,
            "rnm": 8,
        }

        tTXT, tBTN = await util.translate(text="AIO", lang_code=lang_code)

        if data1 in ["met", "pre", "com"]:
            data_1 = dataARRANGEMENT.get(data1)
            if isinstance(data_1, int):
                if all_data[data_1] == "{F}":
                    all_data[data_1] = "{T}"
                elif all_data[data_1] == "{T}":
                    all_data[data_1] = "{F}"
            else:
                return
        elif data1 in ["enc", "rnm", "wat"]:
            if data2 == "{F}":
                input_str = await bot.ask(
                    text=tTXT["waitPASS"],
                    chat_id=callbackQuery.from_user.id,
                    reply_to_message_id=callbackQuery.message.id,
                    reply_markup=ForceReply(True, tTXT["waitPASS"]),
                )
                try:
                    await input_str.reply_to_message.delete()
                except:
                    pass
                await input_str.delete()

                if input_str.text and input_str.text != "/exit":
                    data_1 = dataARRANGEMENT.get(data1)
                    all_data[data_1] = "{T}"
            else:
                data_1 = dataARRANGEMENT.get(data1)
                all_data[data_1] = "{F}"
        elif data1 in ["txt", "rot", "for"]:
            options = {
                "txt": ["text", "html", "json", "{F}"],
                "rot": ["rot90", "rot180", "rot270", "{F}"],
                "for": [
                    "format1",
                    "format2v",
                    "format2h",
                    "format3v",
                    "format3h",
                    "format4",
                    "{F}",
                ],
            }
            current_index = options[data1].index(data2)
            next_index = (
                current_index + 1 if not len(options[data1]) == current_index + 1 else 0
            )
            data_1 = dataARRANGEMENT.get(data1)
            if isinstance(data_1, int):
                all_data[data_1] = options[data1][next_index]
            else:
                return

        aio_list_btn = []
        for index, (key, value) in enumerate(tTXT["out_button"].items()):
            btn = [InlineKeyboardButton(key, value)]
            if index + 1 <= len(all_data):
                btn.append(
                    InlineKeyboardButton(
                        tTXT["true"]
                        if all_data[index] == "{T}"
                        else tTXT["false"]
                        if all_data[index] in ["{F}", "{T}"]
                        else all_data[index].upper(),
                        tTXT["out_values"][index].format(F=all_data[index]),
                    )
                )
            else:
                next_key, next_value = list(tTXT["out_button"].items())[index + 1]
                btn.append(InlineKeyboardButton(next_key, next_value))
                aio_list_btn.append(btn)
                break
            aio_list_btn.append(btn)

        if (
            data1 not in ["enc", "rnm", "wat"]
            or all_data[dataARRANGEMENT.get(data1)] == "{F}"
        ):
            return await callbackQuery.message.edit_reply_markup(
                InlineKeyboardMarkup(aio_list_btn)
            )
        else:
            message_data = callbackQuery.message.text.split("•")
            inPassword, outName, watermark, outPassword = message_data[1::2]

            return await callbackQuery.message.edit(
                text=tTXT["passMSG"].format(
                    callbackQuery.message.reply_to_message.document.file_name,  # password 300 char limit
                    await render.gSF(
                        callbackQuery.message.reply_to_message.document.file_size
                    ),
                    inPassword,
                    input_str.text if data1 == "rnm" else outName,
                    input_str.text if data1 == "wat" else watermark,
                    input_str.text if data1 == "enc" else outPassword,
                ),
                reply_markup=InlineKeyboardMarkup(aio_list_btn),
            )
    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
