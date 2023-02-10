# fileName: plugins/dm/callBack/inline_query/__index__.py
# copyright ©️ 2021 nabilanavab
fileName = "plugins/dm/callBack/inline_query/__index__.py"

import requests
from configs.log     import log
from logger          import logger
from .default        import lang_cb
from .               import inline_data
from bs4             import BeautifulSoup
from .query          import create_result
from pyrogram        import Client as ILovePDF

@ILovePDF.on_inline_query()
async def setLang(bot, inline_query):
    try:
        global inline_data
        
        if log.LOG_CHANNEL and inline_query.query != "":
            query = inline_query.query.replace(" ", "-")
            # replace this with the actual URL of the PDF file on PDF Drive
            # url = f"https://www.pdfdrive.com/{query}-books.html"
            url = f"https://www.pdfdrive.com/search?q={query}"
            
            firstSOUP = BeautifulSoup(requests.get(url).content, 'html.parser')
            
            data = {}
            for i, a in enumerate(firstSOUP.find_all("div", {"class":"col-sm"}), start=1):
                data[i] = dict()
                data[i]["id"] = a.a.get_attribute_list("data-id")[0]
                data[i]["href"] = a.a.get_attribute_list("href")[0]
                
                span = ""
                infos = a.find_all("span")
                for info in infos:
                    span += info.text
                
                data[i]["span"] = span
                data[i]["thumb"] = a.img.get_attribute_list("src")[0]
                data[i]["title"] = a.img.get_attribute_list("title")[0]
            
            inline_data[inline_query.from_user.id] = data
            answer = await create_result(data, inline_query.query)
            if data != dict():
                return await inline_query.answer(
                    cache_time = 1,
                    results = answer,
                    is_gallery = False
                )
        
        answer = await lang_cb(inline_query)
        return await inline_query.answer(
            results = answer, is_gallery = True
        )
        
    except Exception as e:
        logger.exception("🐞 %s: %s" %(fileName, e), exc_info = True)
