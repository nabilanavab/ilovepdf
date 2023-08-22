# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/plugins/dm/callBack/__index__.py"

from plugins import *
from plugins.utils import *
from .file_process import *
from configs.config import images


index = filters.create(lambda _, __, query: query.data.startswith("#"))
@ILovePDF.on_callback_query(index)
async def __index__(bot, callbackQuery):
    try:
        data = callbackQuery.data[1:]
        lang_code = await util.getLang(callbackQuery.message.chat.id)

        if await render.header(bot, callbackQuery, lang_code=lang_code):
            return

        CHUNK, _ = await util.translate(
            text="INDEX", button="INDEX['button']", lang_code=lang_code
        )

        if data == "metadata" and "•" in callbackQuery.message.text:
            return await callbackQuery.answer(CHUNK["readAgain"])

        elif (
            not callbackQuery.message.reply_to_message
            and callbackQuery.message.reply_to_message.document
        ):
            await work.work(callbackQuery, "delete", False)
            return await callbackQuery.message.reply_text(
                "#old_queue 💔\n\n`try by sending new file`", reply_markup=_, quote=True
            )

        elif data == "rot360":
            # Rotating a PDF by 360 degrees will result in the same orientation as the original document.
            # Therefore, returning a useless callback answer
            return await callbackQuery.answer(CHUNK["rot360"])

        elif data in ["ocr"] and "•" in callbackQuery.message.text:
            number_of_pages = callbackQuery.message.text.split("•")[1]
            if int(number_of_pages) >= 5:
                return await callbackQuery.answer(CHUNK["largeNo"])

        elif data == "ocr":
            if ocrPDF.nabilanavab:  # Never Work OCR if nabilanavab==True
                return await callbackQuery.answer(
                    CHUNK["ocrError"]
                )  # Deploy From Docker Files (else OCR never works)

        elif (
            data == "decrypt"
            and "•" in callbackQuery.message.text
            and "🔐" not in callbackQuery.message.text
        ):
            return await callbackQuery.answer(CHUNK["notEncrypt"])

        # create a brand new directory to store all of your important user data
        cDIR = await work.work(callbackQuery, "create", False)
        if not cDIR:
            return await callbackQuery.answer(CHUNK["inWork"])
        await callbackQuery.answer(CHUNK["process"])

        # Asks password for encryption, decryption
        if data in ["decrypt", "encrypt"]:
            notExit, password = await encryptPDF.askPassword(
                bot,
                callbackQuery,
                question=CHUNK["pyromodASK_1"],
                process="Decryption 🔓" if data == "decrypt" else "Encryption 🔐",
            )
            if not notExit:
                await work.work(callbackQuery, "delete", False)
                return await password.reply(CHUNK["exit"], quote=True)
        elif data == "rename":
            notExit, newName = await renamePDF.askName(
                bot, callbackQuery, question=CHUNK["pyromodASK_2"]
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if not notExit:
                await work.work(callbackQuery, "delete", False)
                return await newName.reply(CHUNK["exit"], quote=True)
        elif data in ["header", "footer"]:
            notExit, hfData = await pdfHeader.askText(
                bot, callbackQuery, question=CHUNK["pyromodASK_2"]
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if not notExit:
                await work.work(callbackQuery, "delete", False)
                return await hfData.reply(CHUNK["exit"], quote=True)
        elif data == "merge":
            notExit, mergeId = await mergePDF.askPDF(
                bot,
                callbackQuery,
                question=CHUNK["pyromodASK_3"],
                size=CHUNK["sizeLoad"],
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if not notExit:
                await work.work(callbackQuery, "delete", False)
                return await mergeId.reply(CHUNK["exit"], quote=True)
        # ends with a means all pages.. so no questions
        elif (data.startswith("p2img") and not data.endswith("A")) or data.startswith(
            tuple(["split", "deletePg"])
        ):
            notExit, imageList = await pdfToImages.askimageList(
                bot,
                callbackQuery,
                question=CHUNK["askImage"],
                limit=int(callbackQuery.message.text.split("•")[1])
                if "•" in callbackQuery.message.text
                else 1000,
            )
            if not notExit:
                await work.work(callbackQuery, "delete", False)
                return await imageList.reply(
                    CHUNK["pdfToImgError"].format(
                        callbackQuery.message.text.split("•")[1]
                        if "•" in callbackQuery.message.text
                        else "_"
                    ),
                    quote=True,
                )
        elif data.startswith("wa"):
            if data.startswith("wa|txt"):
                question = CHUNK["watermark_txt"]
            elif data.startswith("wa|img"):
                question = CHUNK["watermark_img"]
            elif data.startswith("wa|pdf"):
                question = CHUNK["watermark_pdf"]
            notExit, watermark = await watermarkPDF.askWatermark(
                bot, callbackQuery, question=question, data=data
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if not notExit:
                await work.work(callbackQuery, "delete", False)
                return await watermark.reply(CHUNK["exit"], quote=True)
        elif data == "partPDF":
            notExit, splitData = await partPDF.askPartPdf(
                bot, callbackQuery, question=CHUNK["pyromodASK_4"],
                limit=int(callbackQuery.message.text.split("•")[1])
                if "•" in callbackQuery.message.text else None
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if not notExit:
                await work.work(callbackQuery, "delete", False)
                return await splitData[0].reply(
                    CHUNK["pdfSplitError"].format(
                        callbackQuery.message.text.split("•")[1]
                        if "•" in callbackQuery.message.text
                        else "_",
                        splitData[1].text if isinstance(splitData[1], str) else splitData[1]
                    ),
                    quote=True,
                )

        dlMSG = await callbackQuery.message.reply_text(
            CHUNK["download"], reply_markup=_, quote=True
        )

        # download the mentioned PDF file with progress updates
        input_file = await bot.download_media(
            message=callbackQuery.message.reply_to_message.document.file_id,
            file_name=f"{cDIR}/inPut.pdf",
            progress=render.progress,
            progress_args=(
                callbackQuery.message.reply_to_message.document.file_size,
                dlMSG,
                time.time(),
            ),
        )

        await dlMSG.edit(text=CHUNK["completed"], reply_markup=_)

        # The program checks the size of the file and the file
        # on the server to avoid errors when canceling the download
        if (
            os.path.getsize(input_file)
            != callbackQuery.message.reply_to_message.document.file_size
        ):
            return await work.work(callbackQuery, "delete", False)

        # The program is designed to check the presence of the "•" character in the message callback query.
        # If it is present,The file has been manipulated one or more times on the server and has attached metadata..
        # If not, the program prompts the user to add metadata to the file.
        # This helps to ensure the proper handling of the file and prevent errors during the manipulation process.
        if "•" not in callbackQuery.message.text:
            checked, number_of_pages = await render.checkPdf(
                input_file, callbackQuery, lang_code
            )
            if data == "decrypt" and checked != "encrypted":
                await work.work(callbackQuery, "delete", False)
                return await dlMSG.edit(CHUNK["notEncrypt"])
        else:
            number_of_pages = int(callbackQuery.message.text.split("•")[1])

        if data == "metadata":
            # After the metadata has been added, the progress message will be deleted
            await work.work(callbackQuery, "delete", False)
            return await dlMSG.delete()

        elif data == "rename":
            isSuccess, output_file = await renamePDF.renamePDF(input_file=input_file)

        elif data == "partPDF":
            isSuccess, output_file = await partPDF.partPDF(
                input_file=input_file, cDIR=cDIR, part=splitData.text
            )

        elif data == "header":
            isSuccess, output_file = await pdfHeader.pdfHeader(
                input_file=input_file, cDIR=cDIR, text=hfData.text
            )

        elif data == "footer":
            isSuccess, output_file = await pdfFooter.pdfFooter(
                input_file=input_file, cDIR=cDIR, text=hfData.text
            )

        elif data == "ocr":
            isSuccess, output_file = await ocrPDF.ocrPDF(
                input_file=input_file,  cDIR=cDIR
            )

        elif data == "baw":
            isSuccess, output_file = await blackAndWhitePdf.blackAndWhitePdf(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "urlRemover":
            isSuccess, output_file = await urlRemover.urlRemover(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "sat":
            isSuccess, output_file = await saturatePDF.saturatePDF(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "1-format":
            isSuccess, output_file = await formatPDF.formatPDF(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "2-format-V":
            isSuccess, output_file = await twoPagesToOne.twoPagesToOne(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "2-format-H":
            isSuccess, output_file = await twoPagesToOneH.twoPagesToOneH(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "3-format-V":
            isSuccess, output_file = await threePagesToOne.threePagesToOne(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "3-format-H":
            isSuccess, output_file = await threePagesToOneH.threePagesToOneH(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "4-format":
            isSuccess, output_file = await combinePages.combinePages(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "draw":
            isSuccess, output_file = await drawPDF.drawPDF(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "zoom":
            isSuccess, output_file = await zoomPDF.zoomPDF(
                cDIR=cDIR, input_file=input_file
            )

        elif data == "encrypt":
            isSuccess, output_file = await encryptPDF.encryptPDF(
                cDIR=cDIR, input_file=input_file, password=password.text
            )

        elif data == "decrypt":
            isSuccess, output_file = await decryptPDF.decryptPDF(
                cDIR=cDIR, input_file=input_file, password=password.text
            )

        elif data == "compress":
            isSuccess, output_file = await compressPDF.compressPDF(
                cDIR=cDIR, input_file=input_file, returnRatio=True
            )

        elif data == "preview":
            isSuccess, output_file = await previewPDF.previewPDF(
                cDIR=cDIR,
                input_file=input_file,
                cancel=_,
                editMessage=dlMSG,
                callbackQuery=callbackQuery,
            )

        elif data == "split":
            isSuccess, output_file = await splitPDF.splitPDF(
                cDIR=cDIR, input_file=input_file, imageList=imageList
            )

        elif data == "deletePg":
            isSuccess, output_file = await deletePDFPg.deletePDFPg(
                cDIR=cDIR, input_file=input_file, imageList=imageList
            )

        elif data == "merge":
            isSuccess, output_file = await mergePDF.mergePDF(
                cDIR=cDIR,
                input_file=input_file,
                text=CHUNK,
                mergeId=mergeId,
                bot=bot,
                dlMSG=dlMSG,
                callbackQuery=callbackQuery,
            )

        elif data == "textM":
            isSuccess, output_file = await messagePDF.messagePDF(
                cDIR=cDIR,
                input_file=input_file,
                text=CHUNK,
                callbackQuery=callbackQuery,
                dlMSG=dlMSG,
            )

        elif data == "inv":
            isSuccess, output_file = await invertPDF.invertPDF(
                cDIR=cDIR, input_file=input_file
            )

        elif data.startswith("rot"):
            isSuccess, output_file = await rotatePDF.rotatePDF(
                cDIR=cDIR, input_file=input_file, angle=data
            )

        elif data.startswith("text") and data != "textM":
            isSuccess, output_file = await textPDF.textPDF(
                cDIR=cDIR, input_file=input_file, data=data
            )

        elif data.startswith(tuple(["p2img|I", "p2img|D"])):
            isSuccess, output_file = await pdfToImages.pdfToImages(
                cDIR=cDIR,
                input_file=input_file,
                text=CHUNK,
                callbackQuery=callbackQuery,
                dlMSG=dlMSG,
                imageList=imageList if not data.endswith("A") else "all",
            )

        elif data.startswith(tuple(["p2img|zip", "p2img|tar"])):
            isSuccess, output_file = await zipTarPDF.zipTarPDF(
                cDIR=cDIR,
                input_file=input_file,
                text=CHUNK,
                callbackQuery=callbackQuery,
                dlMSG=dlMSG,
                imageList=imageList if not data.endswith("A") else "all",
            )

        elif data.startswith("wa"):
            isSuccess, output_file = await watermarkPDF.watermarkPDF(
                cDIR=cDIR,
                input_file=input_file,
                callbackQuery=callbackQuery,
                watermark=watermark,
                text=CHUNK["adding_wa"],
            )

        elif data.startswith("spP"):
            isSuccess, output_file = await stampPDF.stampPDF(
                cDIR=cDIR, input_file=input_file, data=data
            )

        if isSuccess == "finished":
            # The condition isSuccess == "finished" indicates that all the work that needed to be
            # done by the function has been completed and there is no need to send any other files
            await work.work(callbackQuery, "delete", False)
            return (
                await dlMSG.delete()
                if not data.startswith(tuple(["p2img", "textM"]))
                else ""
            )
        elif not isSuccess:
            await work.work(callbackQuery, "delete", False)
            if data == "decrypt":
                return await dlMSG.edit(text=CHUNK["decrypt_error"].format(output_file))
            elif data == "compress":
                return await dlMSG.edit(text=CHUNK["cantCompress"])
            return await dlMSG.edit(text=CHUNK["error"].format(output_file))

        # getting thumbnail
        FILE_NAME, FILE_CAPT, THUMBNAIL = await fncta.thumbName(
            callbackQuery.message,
            callbackQuery.message.reply_to_message.document.file_name
            if data != "rename"
            else newName.text,
        )
        if images.PDF_THUMBNAIL != THUMBNAIL:
            location = await bot.download_media(
                message=THUMBNAIL, file_name=f"{cDIR}/temp.jpeg"
            )
            THUMBNAIL = await formatThumb(location)

        # caption for "encrypt", "rename"
        if data == "encrypt":
            arg = [number_of_pages, password.text]
        elif data == "rename":
            arg = [
                callbackQuery.message.reply_to_message.document.file_name,
                newName.text,
            ]
        elif data == "compress":
            arg = isSuccess
        else:
            arg = None
        _caption = await caption.caption(data=data, lang_code=lang_code, args=arg)

        try:
            await dlMSG.edit(CHUNK["upload"], reply_markup=_)
        except Exception:
            pass

        if data.startswith(tuple(["text", "p2img"])):
            if data.startswith("p2img"):
                data = data[:-1]
            ext = {
                "textT": ".txt",
                "textH": ".html",
                "textJ": ".json",
                "p2img|zip": ".zip",
                "p2img|tar": ".tar",
            }
            FILE_NAME = FILE_NAME[:-4] + ext[data]

        await callbackQuery.message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)

        if data == "partPDF":
            docs = [os.path.join(cDIR, file) for file in os.listdir(cDIR)]
            docs.sort(key=os.path.getctime)
            for _index, _file in enumerate(docs):
                await callbackQuery.message.reply_document(
                    file_name=FILE_NAME
                    if os.path.splitext(FILE_NAME)[1]
                    else f"{FILE_NAME}_{_index}.pdf",
                    document=_file,
                    thumb=THUMBNAIL,
                    caption=f"`part: {_index+1}`\n\n{FILE_CAPT}",
                    progress=render._progress,
                    progress_args=(dlMSG, time.time()),
                )
            await dlMSG.edit("👇")
            await callbackQuery.message.reply_text("👆", quote=True)
        else:
            await callbackQuery.message.reply_document(
                file_name=FILE_NAME
                if os.path.splitext(FILE_NAME)[1]
                else f"{FILE_NAME}.pdf",
                quote=True,
                document=output_file,
                thumb=THUMBNAIL,
                caption=f"{_caption}\n\n{FILE_CAPT}",
                progress=render._progress,
                progress_args=(dlMSG, time.time()),
            )
            await dlMSG.delete()
        await work.work(callbackQuery, "delete", False)

    except Exception as Error:
        logger.exception("🐞 %s: %s" % (file_name, Error), exc_info=True)
        await work.work(callbackQuery, "delete", False)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
