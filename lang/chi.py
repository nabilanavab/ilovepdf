# LANG: CHINESE LANG_CODE: CHI                                      >>  copyright ©️ 2021 nabilanavab  <<                                         fileName : lang/CHI.py
#                                        Thank: nabilanavab                                                   E-mail: nabilanavab@gmail.com

from configs.config import settings

# PM 欢迎信息（家 A:,B:,C:,D...）
HOME = {
    "HomeA" : """嘿 [{}](tg://user?id={})..!!
这个机器人将帮助你用 pdf 做很多事情🥳

一些主要功能是:\n◍ `将图像转换为 PDF`
◍ `将 PDF 转换为图像`\n◍ `将文件转换为 pdf`""",
    "HomeACB" : {
        "⚙️设置⚙️" : "Home|B","⚠️帮助⚠️" : "Home|C",
        "📢 频道📢" : f"{str(settings.SOURCE_CODE)}",
        "🌟 源代码🌟" : f"{str(settings.SOURCE_CODE)}",
        "🚶 关闭 🚶" : "close|mee"
    },
    "HomeAdminCB" : {
        "⚙️设置⚙️" : "Home|B", "⚠️帮助⚠️" : "Home|C",
        "📢 频道📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 源代码🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 STATUS 🗽" : f"status|home", "🚶 关闭 🚶": "close|mee"
    },
    "HomeB":"""设置页面⚙️\n\n用户名:{}
用户 ID:{}\n用户名:{}\n加入日期:{}\n
语言:{}\nAPI:{}
THUMB : {}\nCAPTION : {}\n文件名 : {}""",
    "HomeBCB" : {
        "🌍 LANG 🌍" : "set|lang", "📍 THUMB 📍" : "set|thumb",
        "📈 NAME 📈" : "set|fname", "💩 API 💩" : "set|api",
        "📅 CAPTION 📅" : "set|capt", "« 返回首页 «" : "Home|B2A"
    },
    "HomeC" : """🪂 **帮助消息** 🪂:

```一些主要特点是:
 ◍ 将图像转换为 PDF\n ◍ PDF Manupultions\n ◍ 许多流行的编解码器到 pdf
 
修改pdf文件:
 ◍ PDF⥃IMAGES [all,range,pages]\n ◍ DOCS 到 PDF [png, jpg, jpeg]\n ◍ IMAGES⥃PDF\n ◍ PDF METADATA\n ◍ PDF⥃TEXT\n ◍ TEXT⥃PDF\n ◍压缩pdf文件
 ◍ 拆分 PDF [范围,页数]\n ◍ 合并 PDF\n ◍ 添加邮票\n ◍ 重命名 PDF\n ◍ 旋转 PDF\n ◍ 加密/解密 PDF\n ◍ PDF 格式化 \n ◍ PDF⥃JSON/TXT 文件
 ◍ PDF⥃HTML [网页视图]\n ◍ URL⥃PDF\n ◍ PDF⥃ZIP/TAR/RAR [所有:,范围:,页面]\n还有更多.. ``""",
    "HomeCCB" : {"« 返回首页 «" : "Home|A", "🛈 使用说明 🛈" : "Home|D"},
    "HomeD" : """`由于这是一项免费服务,我无法保证我能维持多久..`😝
 
⚠️使用说明⚠️:
🛈 __请不要试图滥用机器人管理员__ 😒
🛈 __不要在这里发送垃圾邮件,可能会导致永久禁止 🎲__。
🛈 __Porn 内容也会给你永久禁令💯__

**发送任何图片开始:** 😁""",
    "HomeDCB" : {"⚠️ HELP ⚠️" : "Home|C", "» BACK HOME »" : "Home|A"}
}

SETTINGS = {
    "default" : ["默认❌","自定义✅"],"chgLang":{"设置⚙️ » 更改语言🌐":"nabilanavab"},
    "error" : "从数据库中检索数据时出现问题", "lang" : "现在,选择任何语言..",
    "ask" : ["Now, Send me..", "Now, Send me.. 😅\n\nFast.! 我没时间复习文本了.. "],
    "askApi" : "\n\n打开下面的链接并将密码发送给我:", "waitApi" : {"打开链接 ✅" : "https://www.convertapi.com/a/signin"},
    "wait" : {"等待..🥱":"nabilanavab"},"back":{"« 返回首页 «":"Home|B2S"},"errorCB":{"« 返回首页 «":"Home|B2A"},
    "result" : ["设置无法更新❌", "设置更新成功✅"], "cant" : "此功能无法使用❌",
    "feedback" : "像你这样的优秀客户的评论帮助了其他人。\n@nabilanavab"
                 "\n\n报告 {} 语言中的错误:\n`• 指定语言\n• 错误消息\n• 新消息`",
    "feedbtn" : {"Report Lang Error" : settings.REPORT},
    "thumb" : [
        {" 设置⚙️ » 缩略图📷 " : "nabilanavab", "♻ 更改 ♻" : "set|thumb+", "« 返回首页 «" : "Home|B"},
        {" 设置⚙️ » 缩略图📷 ":"nabilanavab","♻ 更改 ♻":"set|thumb+","🗑 删除 🗑":"set|thumb-","« 返回首页 «":"Home|B2S"}
    ],
    "fname" : [
        {"SETTING ⚙️ » FNAME 📷" : "nabilanavab", "♻ 更改 ♻" : "set|fname+", "« 返回首页 «" : "Home|B2S"},
        {"SETTING ⚙️ » FNAME 📷" : "nabilanavab", "♻ 更改 ♻" : "set|fname+", "🗑 删除 🗑" : "set|fname-", "« 返回首页 «" : "Home|B2S"}
    ],
    "api" : [
        {"SETTING ⚙️ » API 📷" : "nabilanavab", "♻ 更改 ♻" : "set|api+", "« 返回首页 «" : "Home|B2S"},
        {"SETTING ⚙️ » API 📷" : "nabilanavab", "♻ 更改 ♻" : "set|api+", "🗑 删除 🗑" : "set|api-", "« 返回首页 «" : "Home|B2S"}
    ],
    "capt" : [
        {"SETTING ⚙️ » CAPTION 📷" : "nabilanavab", "♻ 更改 ♻" : "set|capt+", "« 返回首页 «" : "Home|B2S"},
        {"SETTING ⚙️ » CAPTION 📷" : "nabilanavab", "♻ 更改 ♻" : "set|capt+", "🗑 删除 🗑" : "set|capt-", "« 返回首页 «" : "Home|B2S"}
    ]
}

BOT_COMMAND = {"start" : "欢迎信息..", "txt2pdf" : "创建文本 PDF"}

HELP_CMD = {
    "userHELP" : """[用户命令消息]:\n
/start: 检查 Bot 是否存活\n/cancel: 取消当前工作
/delete: 清除图像到 pdf 队列\n/txt2pdf: 文本到 pdf""",
    "adminHelp" : """\n\n\n[管理命令消息]:\n
/send: 广播, pm message""",
    "footerHelp" : f"""\n\n\n源代码: [i 💜 PDF]({str(settings.SOURCE_CODE)})
机器人:@complete_pdf_bot 💎\n[支持频道]({settings.OWNED_CHANNEL})""",
    "CB":{ "⚠️关闭⚠️" : "关闭|全部" }
}

STATUS_MSG = {
    "HOME" : "`现在,选择下面的任何选项以获取当前状态💱..`",
    "_HOME" : {
        "📊 ↓ SERVER ↓ 📊" : "nabilanavab","📶 STORAGE 📶" : "status|server",
        "🥥 DATABASE 🥥" : "status|db", "🌝 ↓ GET LIST ↓ 🌝": "nabilanavab",
        "💎 ADMIN 💎" : "status|admin","👤 用户 👤" : "status|users",
        "« 返回 «" : "Home|A"
    },
    "DB" : """📂 数据库 :\n\n**◍ 数据库用户 :** `{}` 📍\n**◍ 数据库聊天 :** `{}` 📍""",
    "SERVER" : """**◍总空间:**`{}`
**◍ 已用空间:** `{}({}%)`\n**◍ 可用空间:** `{}`
**◍ CPU 使用率:** `{}`%\n**◍ RAM 使用率:** `{}`%
**◍ 当前工作:** `{}`\n**◍ 消息 ID:** `{}`""",
    "BACK" : {"« BACK «" : "status|home"}, "ADMIN" : "**Total ADMIN:** __{}__\n",
    "USERS" : "保存在 DB 中的用户是:\n\n", "NO_DB" : "还没有设置数据库 💩"
}

feedbackMsg = f"[写反馈📋]({settings.FEEDBACK})"

# 群欢迎消息
HomeG = {
    "HomeA" : """你好！🖐️\n我是新来的 {message.chat.title}\n
让我自我介绍一下..\n我的名字是 iLovePDF,我可以帮你做很多事情
@Telegram PDF 文件的事情\n\n感谢 @nabilanavab 这个 Awesome Bot 😅""",
    "HomeACB":{
        "🤠 BOT OWNER 🤠": f"https://telegram.dog/{settings.OWNER_USERNAME}",
        "🛡️ 更新频道 🛡️":f"{settings.OWNED_CHANNEL}","🌟 源代码 🌟":f"{str(settings.SOURCE_CODE)}"
    }
}

# 禁止用户界面
BAN = {
    "cbNotU" : "消息不是给你的.. 😏",
    "banCB" : {
        "创建你自己的机器人" : f"{str(settings.SOURCE_CODE)}", "教程" : f"{str(settings.SOURCE_CODE)}",
        "更新频道" : "https://telegram.dog/ilovepdf_bot"
    },
    "UCantUse" : """嘿{}\n\n由于某些原因你不能使用这个 BOT :(""",
    "UCantUseDB" : """嘿{}\n\n由于某些原因你不能使用这个 BOT :(\n\nREASON: {}""",
    "GroupCantUse" : """{} 永远不要期望我有好的回应\n
管理员限制我在这里工作.. 🤭""",
    "GroupCantUseDB" : """{} 永远不要期望我有好的回应\n
管理员限制我在这里工作.. 🤭\n\n原因:{}""",
    "Force" : """等待 [{}](tg://user?id={})..!!\n
由于巨大的流量,只有频道成员可以使用这个机器人🚶\n
这意味着您需要加入下面提到的频道才能使用我！\n
加入后点击`"♻️ 刷新 ♻️"`..😅""",
    "ForceCB" : {"🌟 加入频道 🌟" : "{}","♻️ 刷新 ♻️" : "刷新"},
    "Fool" : "你骗不了我..🤭"
}

checkPdf = {
    "pg" : "`页数:•{}•` 🌟",
    "pdf" : """`我应该如何处理这个文件？`\n\n文件名 : `{}`\n文件大小 : `{}`""",
    "pdfCB" : {
        "⭐ META£ATA ⭐":"metaData","🗳️ PREVIEW 🗳️":"preview",
        "🖼️ 图像 🖼️":"pdf|img","✏️ 文本 ✏️":"pdf|txt",
        "🔐 加密 🔐":"work|encrypt","🔒 解密 🔓":"work|decrypt",
        "🗜️ 压缩 🗜️":"work|compress","🤸 旋转 🤸":"pdf|rotate",
        "✂️ SPLIT ✂️":"pdf|split","🧬 MERGE 🧬":"merge","™️ STAMP ™️":"pdf|stp",
        "✏️ 重命名 ✏️":"work|rename", "📝 OCR 📝" : "work|ocr",
        "🥷 A4 格式 🥷":"work|format", "🚫 关闭 🚫" : "close|all"
    },
    "error" : """__我没有对这个文件做任何事情__ 😏\n\n🐉 `CODEC ERROR` 🐉""",
    "errorCB":{"❌ 编解码器中的错误 ❌" : "error","🔸 关闭 🔸 " : "close|all"},
    "encrypt" : """`文件已加密`🔐\n\n文件名: `{}`\n文件大小: `{}`""",
    "encryptCB" : {"🔓 DECRYPT 🔓" : "work|decrypt"}
}

PROGRESS = {
    "progress" : """**\n完成✅ : **{0}/{1}\n**速度🚀:** {2}/s\n**预计时间⏳:** {3}""",
    "dlImage" : "`正在下载你的图片..⏳`", "upFile" : "`开始上传..`📤",
    "dlFile" : "`正在下载你的文件..` 📥", "upFileCB" : {"📤 .. UPLOADING..📤" : "nabilanavab"},
    "workInP":"正在进行中..🙇", "refresh" : {"♻️ 刷新 ♻️" : "{}"},
    "takeTime" : """```⚙️ 正在进行中..`\n`可能需要一些时间..```💛""",
    "cbPRO_D" : ["📤 下载: {:.2f}% 📤", "🎯 取消🎯"], "cbPRO_U" : ["📤 上传: {:.2f}% 📤", "🎯 取消🎯"]
}

GENERATE = {
    "deleteQueue" : "`队列删除成功..`🤧", "noQueue" : "`没有建立队列..`😲",
    "noImages" : "没有建立图像。!! 😒", "getFileNm" : "现在给我发一个文件名😒:",
    "geting" : "文件名: `{}`\n页面: `{}`", "getingCB" : {"📚 GENERATING PDF.." : "nabilanavab"},
    "currDL" : "已下载 {} 图片 🥱"
}

document = {
    "refresh" : PROGRESS['refresh'],"inWork" : PROGRESS['workInP'],"reply":checkPdf['pdf'],
    "replyCB" : checkPdf['pdfCB'],"download" : PROGRESS['dlFile'],"process" : "⚙️ 处理..",
    "takeTime":PROGRESS['takeTime'],"upFile":PROGRESS['upFile'],"dlImage":PROGRESS['dlImage'],
    "big" : """由于过载,所有者限制 pdf 文件的 {}mb 🙇
\n`请给我发送一个小于 {}mb Size` 的文件🙃""",
    "bigCB" : {"💎 创建 2Gb 支持机器人💎" : "https://github.com/nabilanavab/ilovepdf"},
    "imageAdded" : """`将 {} 页/'添加到您的 pdf..`🤓\n\nfileName: `{}.pdf`""",
    "setHdImg" : """现在 Image To PDF 处于高清模式😈""",
    "setDefault":{"« 返回默认质量 «" "close|hd"},
    "error" : """出了点问题.. 🐉\n\n错误:`{}`""",
    "noAPI" : "`请添加转换 API.. 💩\n\n开始 » 设置 » api » 添加/更改`",
    "useDOCKER" : "`不支持文件,使用 docker 部署机器人`",
    "fromFile" : "`Converted: {} to {}`", "unsupport" : "`不支持的文件..🙄`",
    "generateRN":{"生成 📚" : "generate", "重命名 ✍️" : "generateREN"},
    "generate" : {"生成 📚" : "generate"}, "cancelCB" : { "⟨ 取消 ⟩" : "close|me"}
}

noHelp = f"`没有人会帮助你`😏"

split = {
    "inWork":PROGRESS['workInP'],"cancelCB": document['cancelCB'],
    "download":PROGRESS['dlFile'],"exit":"`进程已取消..`😏",
    "buttom" : {
        "⚙️ PDF » SPLIT ↓" : "nabilanavab", "范围内 🦞" : "split|R",
        "单页 🐛" : "split|S", "« BACK «" : "pdf"
    },
    "work" : ["Range", "Single"], "over" : "`5 次尝试结束.. 进程取消..`😏",
    "pyromodASK_1" : """__Pdf Split » 按范围\n现在,输入范围（开始:结束）:__
\n/exit __to cancel__""",
    "已完成" : "`下载完成..` ✅",
    "error_1" : "`语法错误:justNeedStartAndEnd `🚶",
    "error_2" : "`语法错误:errorInEndingPageNumber `🚶",
    "error_3" : "`语法错误:errorInStartingPageNumber `🚶",
    "error_4" : "`语法错误:pageNumberMustBeADigit` 🧠",
    "error_5" : "`语法错误:noEndingPageNumber 或 notADigit` 🚶",
    "error_6" : "`找不到任何数字..`😏",
    "error_7" : "`出错了..`😅", "error_8" : "`输入小于 {} 的数字..`😏",
    "error_9":"`第一次检查页数`😏","upload":"⚙️ `开始上传..`📤"
}

pdf2IMG = {
    "inWork":PROGRESS['workInP'],"process":document['process'],
    "download":PROGRESS['dlFile'],"uploadFile":split['upload'],
    "toImage" : {
        "⚙️ PDF » 图像 ↓":"nabilanavab","🖼 IMG 🖼":"pdf|img|img",
        "📂 DOC 📂" : "pdf|img|doc", "🤐 ZIP 🤐" : "pdf|img|zip",
        "🎯 TAR 🎯" : "pdf|img|tar", "« 返回 «" : "pdf"
    },
    "imgRange" : {
        "⚙️ PDF » 图像 » {} ↓" : "nabilanavab", "🙄 ALL 🙄" : "p2img|{}A",
        "🤧 RANGE 🤧" : "p2img|{}R", "🌝 PAGES 🌝" : "p2img|{}S", "« 返回 «" : "pdf|img"
    },
    "over":"`5 次尝试结束.. 进程取消..`😏",
    "pyromodASK_1" : """__Pdf - Img›Doc » 页数:\n现在,输入范围（开始:结束）:__
\n/exit __to cancel__""",
    "pyromodASK_2" : """"__Pdf - Img›Doc » 页数:\n现在,输入由__ (,) 分隔的页码:
\n/exit __to cancel__""",
    "exit" : "`进程取消..`😏",
    "error_1" : "`语法错误:justNeedStartAndEnd `🚶",
    "error_2" : "`语法错误:errorInEndingPageNumber `🚶",
    "error_3" : "`语法错误:errorInStartingPageNumber `🚶",
    "error_4" : "`语法错误:pageNumberMustBeADigit` 🧠",
    "error_5" : "`语法错误:noEndingPageNumber 或 notADigit` 🚶",
    "error_6" : "`找不到任何号码..`😏", "error_7" : "`出错了..`😅",
    "error_8" : "`PDF 只有 {} 页`💩", "error_9" : "`第一次检查页数`😏",
    "error_10" : "__由于某些限制 Bot 仅以 ZIP 格式发送 50 页..__😅",
    "total" : "`总页数:{}..⏳`", "upload" : "`上传中:{}/{} 页..🐬`",
    "current" : "`Converted: {}/{} pages.. 🤞`", "complete" : "`上传完成.. `🏌️",
    "canceledAT" : "`在 {}/{} 页取消..` 🙄", "cbAns" : "⚙️ Okeyda,正在取消..",
    "cancelCB" : {"💤 CANCEL 💤" : "close|P2I"}, # EDITABLE: ❌
    "canceledCB" : {"🍄 CANCELED 🍄" : "close|P2IDONE"},
    "completed":{"😎 完成 😎":"close|P2ICOMP"}
}

merge = {
    "inWork":PROGRESS['workInP'],"process":document['process'],"upload":PROGRESS['upFile'],
    "load" : "__由于过载,您一次只能合并 5 个 pdf__",
    "sizeLoad" : "`Due to Overload Bot Only Support %sMb pdfs..", # 删除 %s 显示错误
    "pyromodASK" : """__MERGE pdfs » 队列中的 pdf 总数:{}__

/exit __取消__
/merge __to 合并__""",
    "exit" : "`进程取消..` 😏", "total" : "`PDF 总数 : {} 💡",
    "current" : "__Started Downloading Pdf : {} 📥__", "cancel" : "`合并过程已取消..😏`",
    "started" : "__Merging Started.. __ 🪄", "caption" : "`merged pdf 🙂`",
    "error" : "`可能是文件加密..`\n\n原因:{}"
}

metaData = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "download" : PROGRESS['dlFile'], # [❌]
    "read" : "请再读一遍这条消息.. 🥴"
}

preview = {
    "inWork":PROGRESS['workInP'],"process":document['process'],"error":document['error'],
    "download" : PROGRESS['dlFile'], "_" : "PDF 只有 {} 页 🤓\n\n",
    "__" : "PDF 页数:{}\n\n", "total" : "`总页数:{}..` 🤌",
    "album" : "`正在准备专辑..`🤹", "upload" : f"`上传:预览页面..🐬`"
}

stamp = {
    "stamp" : {
        "⚙️ PDF » STAMP ↓" : "nabilanavab",
        "不公开发布 🤧" : "pdf|stp|10",
        "公开发布 🥱" : "pdf|stp|8",
        "机密 🤫" : "pdf|stp|2", "部门 🤝" : "pdf|stp|3",
        "实验性 🔬":"pdf|stp|4","过期 🐀":"pdf|stp|5",
        "Final 🔧" : "pdf|stp|6", "供评论 🗯️" : "pdf|stp|7",
        "未批准 😒":"pdf|stp|9","已批准 🥳":"pdf|stp|0",
        "已售出 ✊":"pdf|stp|11","绝密 😷":"pdf|stp|12",
        "草稿 👀":"pdf|stp|13","原样 🤏":"pdf|stp|1",
        "« 返回 «" : "pdf"
    },
    "stampA":{
        "⚙️ PDF » 邮票 » 颜色 ↓" : "nabilanavab",
        "红色 ❤️":"spP|{}|r","蓝色 💙":"spP|{}|b",
        "绿色 💚":"spP|{}|g","黄色 💛":"spP|{}|c1",
        "粉红色 💜":"spP|{}|c2","色调 💚":"spP|{}|c3",
        "白色 🤍":"spP|{}|c4","黑色 🖤":"spP|{}|c5",
        "« 返回 «" : "pdf|stp"
    },
    "inWork":PROGRESS['workInP'],"process":document['process'],
    "download":PROGRESS['dlFile'],"upload":PROGRESS['upFile'],
    "stamping":"`Started Stamping..` 💠", "caption":"""stamped pdf\ncolor : `{}`\nannot : `{}`"""
}

work = {
    "inWork":PROGRESS['workInP'], "process":document['process'],
    "download":PROGRESS['dlFile'], "takeTime":PROGRESS['takeTime'],
    "upload":PROGRESS['upFile'], "button":document['cancelCB'],
    "rot360" : "你有一些大问题..🙂", "ocrError" : "所有者受限 😎🤏",
    "largeNo" : "发送少于 5 页的 pdf 文件.. 🙄",
    "pyromodASK_1" : """__PDF {} »\n现在,请输入密码 :__\n\n/exit __to cancel__""",
    "pyromodASK_2" : """__重命名 PDF »\n现在,请输入新名称:__\n\n/exit __to cancel__""",
    "exit" : "`进程取消.. `😏", "ren_caption" : "__New Name:__ `{}`",
    "notENCRYPTED" : "`文件未加密..`👀",
    "compress" : "⚙️ `开始压缩.. 🌡️\n可能需要一些时间..`💛",
    "decrypt" : "⚙️ `开始解密.. 🔓\n可能需要一些时间..`💛",
    "encrypt" : "⚙️ `开始加密.. 🔐\n可能需要一些时间..`💛",
    "ocr" : "⚙️ `添加 OCR 层.. ✍️\n这可能需要一些时间..`💛",
    "format" : "⚙️ `开始格式化.. 🤘\n可能需要一些时间..`💛",
    "rename" : "⚙️ `重命名 PDf.. ✏️\n这可能需要一些时间..`💛",
    "rot" : "⚙️ `旋转 PDf.. 🤸\n这可能需要一些时间..`💛",
    "pdfTxt" : "⚙️ `提取文本..🐾\n可能需要一些时间..`💛",
    "fileNm" : "旧文件名:{}\n新文件名:{}",
    "rotate":{
        "⚙️ PDF » ROTETE ↓" : "nabilanavab", "90°" : "work|rot90", "180°" : "work|rot180",
        "270°" : "work|rot270", "360°" : "work|rot360", "« BACK «" : "pdf"
    },
    "txt" : {
        "⚙️ PDF » TXT ↓" : "nabilanavab", "📜 MESSAGE 📜" : "work|M", "🧾 TXT FIL 🧾" : "work|T",
        "🌐 HTML 🌐" : "work|H", "🎀 JSON 🎀" : "work|J", "« BACK «" : "pdf"
    }
}

PROCESS = {
    "ocr" : "OCR 添加", "decryptError" : "__Cannot Decrypt the file with__ `{}` 🕸️",
    "decrypted" : "__Decrypted File__", "encrypted" : "__Page Number__: {}\n__key__ 🔐: ||{}||",
    "compressed" : """`原始大小 : {}\nCompressed Size : {}\n\nRatio : {:.2f} %`""",
    "cantCompress" : "文件无法压缩更多..🤐",
    "pgNoError" : """__出于某种原因 A4 FORMATTING 支持少于 5 页的 pdf__\n\n总页数: {} ⭐""",
    "ocrError" : "`已经有一个文本层.. `😏",
    "90":"__旋转 90°__","180":"__旋转 180°__","270":"__旋转 270°__",
    "formatted" : "A4 格式文件", "M" : "♻ Extracted {} Pages ♻",
    "H":"HTML 文件","T":"TXT 文件","J":"JSON 文件"
}

pdf2TXT = {
    "upload" : PROGRESS["upFile"], "exit" : split['exit'], "nothing" : "没什么可创建的..😏",
    "TEXT" : "`从短信创建 PDF »`", "start" : "开始将 txt 转换为 Pdf..🎉",
    "font_btn":{
        "TXT@PDF » SET FONT":"nabilanavab","Times":"pdf|font|t","Courier":"pdf|font|c","Helvetica（默认）":"pdf|font|h ",
        "符号":"pdf|font|s","Zapfdingbats":"pdf|font|z","🚫 CLOSE 🚫":"close|me"
    },
    "size_btn" : { "TXT@PDF » {} » SET SCALE" : "nabilanavab", "Portarate" : "t2p|{}|p", "Landscape" : "t2p|{}|l", "« 返回«": "pdf|T2P"},
    "askT" : "__TEXT TO PDF » 现在,请输入标题:__\n\n/exit __to cancel__\n/skip __to skip__",
    "askC" : "__TEXT TO PDF » 现在,请输入段落 {}:__\n\n/exit __to cancel__\n/create __to create__"
}

URL = {
    "get" : {"🧭 获取 PDF 文件🧭" : "getFile"}, "close" : HELP_CMD['CB'], "notPDF" : "`不是 PDF 文件",
    "error" : "🐉 SOMETHING WENT WRONG 🐉\n\n错误:`{}`\n\nNB:在群组中,机器人只能获取加入群组后发送的文档 =)",
    "done" : "```差不多完成了.. ✅\n现在,开始上传.. 📤```", "_error_" : "给我发送任何 url 或直接电报 pdf 链接",
    "openCB" : {"在浏览器中打开" : "{}"}, "_error" : "`有些事情出错了 =(`\n\n`{}`",
    "_get" : "[打开聊天]({})\n\n**关于聊天↓**\n聊天类型:{}\n聊天名称:{}\n聊天用户:@{}\n"
             "聊天 ID:{}\n日期:{}\n\n**关于媒体↓**\n媒体:{}\n文件名:{}\n文件大小:{}\n\n文件类型:{}"
}

getFILE = {
    "inWork" : PROGRESS['workInP'], "big" : "发送小于 {}mb 的 pdf url", "wait" : "等等.. 让我.. 😜",
    "dl":{"📥 ..DOWNLOADING..📥":"nabilanavab"},"up":{"📤..UPLOADING..📤":"nabilanavab"},
    "完成":{"😎完成😎":f"{str(settings.SOURCE_CODE)}"}
}

cbAns = [
    "此功能正在开发中⛷️", "错误 annenn paranjille.. 那么是什么.. 😏",
    "进程已取消..😏","文件未加密..👀","没有任何官方信息..😅","🎉已完成..🏃"
]

inline_query = {
    "TOP":{"现在 , 选择语言➟":"nabilanavab"},"capt":"SET LANGUAGE ⚙️","des":"作者:@nabilanavab ❤"
}
