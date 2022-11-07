# LANG: SPANISH LANG_CODE: SPN                                      >>  copyright ©️ 2021 nabilanavab  <<                                         fileName : lang/SPN.py
#                                        Thank: nabilanavab                                                   E-mail: nabilanavab@gmail.com

from configs.config import settings

# MENSAJE DE BIENVENIDA PM (CASA A, B, C, D...)
HOME = {
    "HomeA": """Hola [{}](tg://user?id={})..!!
Este bot te ayudará a hacer muchas cosas con pdf 🥳

Algunas de las funciones clave son:\n◍ `Convertir imágenes a PDF`
◍ `Convertir PDF a imágenes`\n◍ `Convertir archivos a pdf`""",
    "HomeACB" : {
        "⚙️ AJUSTES ⚙️": "Home|B", "⚠️ AYUDA ⚠️": "Home|C",
        "📢 CANAL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 CÓDIGO FUENTE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🚶 CERRAR 🚶": "close|mee"
    },
    "HomeAdminCB": {
        "⚙️ AJUSTES ⚙️": "Home|B", "⚠️ AYUDA ⚠️": "Home|C",
        "📢 CANAL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 CÓDIGO FUENTE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 ESTADO 🗽" : f"status|home", "🚶 CERRAR 🚶" : "close|mee"
    },
    "HomeB": """PÁGINA DE CONFIGURACIÓN ⚙️\n\nNOMBRE DE USUARIO: {}
ID DE USUARIO: {}\nNOMBRE DE USUARIO: {}\nFECHA DE INGRESO: {}\n
IDIOMA: {}\nAPI: {}
PULGAR: {}\nTÍTULO: {}\nNOMBRE DE ARCHIVO: {}""",
    "HomeBCB" : {
        "🌍 LANG 🌍" : "set|lang", "📍 PULGAR 📍" : "set|thumb",
        "📈 NOMBRE 📈" : "set|fname", "💩 API 💩" : "set|api",
        "📅 TÍTULO 📅" : "set|capt", "« VOLVER A INICIO «" : "Home|B2A"
    },
    "HomeC": """🪂** MENSAJE DE AYUDA** 🪂:

```Algunas de las características principales son:
 ◍ Convertir imágenes a PDF\n ◍ Manufacturas de PDF\n ◍ Muchos códecs populares a pdf
 
Modificar el archivo pdf:
 ◍ PDF⥃IMÁGENES [todo,rango,páginas]\n ◍ DOCS a PDF [png, jpg, jpeg]\n ◍ IMÁGENES⥃PDF\n ◍ PDF METADATOS\n ◍ PDF⥃TEXTO\n ◍ TEXTO⥃PDF\n ◍ Comprimir archivo pdf
 ◍ DIVIDIR PDF [rango, páginas]\n ◍ COMBINAR PDF\n ◍ AÑADIR SELLO\n ◍ RENOMBRAR PDF\n ◍ GIRAR PDF\n ◍ CIFRAR/DECIFRAR PDF\n ◍ FORMATEAR PDF\n ◍ PDF⥃ARCHIVO JSON/TXT
 ◍ PDF⥃HTML [vista web]\n ◍ URL⥃PDF\n ◍ PDF⥃ZIP/TAR/RAR [todas, rango, páginas]\nY mucho más.. ```""",
    "HomeCCB" : {"« VOLVER A INICIO «" : "Home|A", "🛈 INSTRUCCIONES 🛈" : "Home|D"},
    "HomeD": """`Como este es un servicio gratuito, no puedo garantizar cuánto tiempo puedo mantener este servicio..`😝
 
⚠️ INSTRUCCIONES ⚠️:
🛈 __Por favor, no intentes abusar de los administradores de bots__ 😒
🛈 __No envíes spam aquí, puede dar lugar a una prohibición permanente 🎲__.
🛈 __El contenido porno también te dará una PROHIBICIÓN PERMANENTE 💯__

**Envía cualquier imagen para comenzar:** 😁""",
    "HomeDCB" : {"⚠️ AYUDA ⚠️" : "Home|C", "» VOLVER A INICIO »" : "Home|A"}
}

SETTINGS = {
    "default" : ["DEFAULT ❌", "PERSONALIZADO ✅"], "chgLang" : {"AJUSTE ⚙️ » CAMBIAR IDIOMA 🌐" : "nabilanavab"},
    "error": "Algo salió mal al recuperar datos de la base de datos", "lang": "Ahora, seleccione cualquier idioma...",
    "ask" : ["Ahora, envíame...", "Ahora, envíame... 😅\n\n¡Rápido! No tengo más tiempo para repasar el texto... 😏\n\n/cancel: para cancelar "],
    "askApi": "\n\nAbra el siguiente enlace y envíeme el código secreto:", "waitApi": {"Abrir enlace ✅": "https://www.convertapi.com/a/signin"},
    "wait" : {"Esperando.. 🥱" : "nabilanavab"}, "api" : {"« VOLVER A INICIO «" : "Home|B2S"}, "errorCB" : {"« VOLVER A INICIO «" : "Home|B2A"},
    "result": ["La configuración no se puede actualizar ❌", "La configuración se actualizó correctamente ✅"], "cant": "Esta función no se puede usar ❌",
    "feedback": "Reseñas de clientes increíbles como tú ayudan a otros.\n@nabilanavab"
                 "\n\nInformar un ERROR en {} idioma:\n`• Especificar idioma\n• Mensaje de error\n• Nuevo mensaje`",
    "feedbtn": {"Informe de error de idioma": settings.REPORT},
    "thumb" : [
        {"AJUSTES ⚙️ » MINIATURA 📷" : "nabilanavab", "♻ AÑADIR ♻" : "set|thumb+", "« VOLVER A INICIO «" : "Home|B"},
        {"AJUSTE ⚙️ » MINIATURA 📷" : "nabilanavab", "♻ CAMBIAR ♻" : "set|thumb+", "🗑 ELIMINAR 🗑" : "set|thumb-", "« VOLVER A INICIO «" : "Home|B2S"}
    ],
    "fname" : [
        {"AJUSTES ⚙️ » FNAME 📷" : "nabilanavab", "♻ ADD ♻" : "set|fname+", "« VOLVER A INICIO «" : "Home|B2S"},
        {"AJUSTES ⚙️ » FNAME 📷" : "nabilanavab", "♻ CAMBIAR ♻" : "set|fname+", "🗑 ELIMINAR 🗑" : "set|fname-", "« VOLVER A INICIO «" : "Home|B2S"}
    ],
    "api" : [
        {"AJUSTES ⚙️ » API 📷" : "nabilanavab", "♻ AGREGAR ♻" : "set|api+", "« VOLVER A INICIO «" : "Home|B2S"},
        {"AJUSTES ⚙️ » API 📷" : "nabilanavab", "♻ CAMBIO ♻" : "set|api+", "🗑 ELIMINAR 🗑" : "set|api-", "« VOLVER A INICIO «" : "Home|B2S"}
    ],
    "capt" : [
        {"AJUSTES ⚙️ » TÍTULO 📷" : "nabilanavab", "♻ AÑADIR ♻" : "set|capt+", "« VOLVER A INICIO «" : "Home|B2S"},
        {"AJUSTE ⚙️ » TÍTULO 📷" : "nabilanavab", "♻ CAMBIAR ♻" : "set|capt+", "🗑 ELIMINAR 🗑" : "set|capt-", "« VOLVER A INICIO «" : "Home|B2S"}
    ]
}

BOT_COMMAND = {"start": "Mensaje de bienvenida..", "txt2pdf": "Crear PDF de texto"}

HELP_CMD = {
     "userHELP" : """[MENSAJES DE COMANDO DEL USUARIO]:\n
/start: para verificar si Bot está vivo\n/cancel: cancela el trabajo actual
/eliminar: borrar imagen a cola de pdf\n/txt2pdf: texto a pdf""",
     "adminHelp": """\n\n\n[MENSAJES DE COMANDO DEL ADMINISTRADOR]:\n
/enviar: para transmitir, mensaje pm""",
     "footerHelp": f"""\n\n\nCódigo fuente: [i 💜 PDF]({str(settings.SOURCE_CODE)})
Bot: @complete_pdf_bot 💎\n[Canal de soporte]({settings.OWNED_CHANNEL})""",
     "CB": {"⚠️ CERRAR ⚠️": "cerrar|todo"}
}

STATUS_MSG = {
     "HOME": "`Ahora, seleccione cualquier opción a continuación para obtener el estado actual 💱..`",
     "_HOME" : {
         "📊 ↓ SERVIDOR ↓ 📊" : "nabilanavab", "📶 ALMACENAMIENTO 📶" : "estado|server",
         "🥥 BASE DE DATOS 🥥": "status|db", "🌝 ↓ OBTENER LISTA ↓ 🌝": "nabilanavab",
         "💎 ADMINISTRADOR 💎" : "status|admin", "👤 USUARIOS 👤" : "status|users",
         "« VOLVER «" : "Home|A"
     },
     "DB" : """📂 BASE DE DATOS :\n\n**◍ Usuarios de la base de datos :** `{}` 📍\n**◍ Chats de la base de datos :** `{}` 📍""",
     "SERVER": """**◍ Espacio total:** `{}`
**◍ Espacio usado:** `{}({}%)`\n**◍ Espacio libre:** `{}`
**◍ Uso de CPU:** `{}`%\n**◍ Uso de RAM:** `{}`%
**◍ Trabajo actual:** `{}`\n**◍ ID del mensaje:** `{}`""",
     "BACK" : {"« VOLVER «" : "estado|inicio"}, "ADMIN" : "**Total ADMIN:** __{}__\n",
     "USERS": "Los usuarios guardados en la base de datos son:\n\n", "NO_DB": "Todavía no se ha establecido ninguna BASE de datos 💩"
}

feedbackMsg = f"[Escribe un comentario 📋]({settings.FEEDBACK})"

# MENSAJE DE BIENVENIDA DEL GRUPO
HomeG = {
     "HomeA" : """¡Hola! 🖐️\nSoy nuevo aquí {message.chat.title}\n
Déjame presentarme..\nMi nombre es iLovePDF, y puedo ayudarte a hacer muchas
Cosas con archivos PDF de @Telegram\n\nGracias @nabilanavab por este increíble bot 😅""",
     "InicioACB" : {
         "🤠 PROPIETARIO DEL BOT 🤠": f"https://telegram.dog/{settings.OWNER_USERNAME}",
         "🛡️ ACTUALIZAR CANAL 🛡️": f"{settings.OWNED_CHANNEL}", "🌟 CÓDIGO FUENTE 🌟": f"{settings.SOURCE_CODE}"
     }
}

# IU DE USUARIO PROHIBIDO
BAN = {
    "cbNotU": "Mensaje no para ti... 😏",
    "banCB" : {
        "Crea tu Propio Bot": f"{settings.SOURCE_CODE}", "Tutorial": f"{settings.SOURCE_CODE}",
        "Actualizar canal": "https://telegram.dog/ilovepdf_bot"
    },
    "UCantUse" : """Hola {}\n\nPOR ALGUNA RAZÓN NO PUEDES USAR ESTE BOT :(""",
    "UCantUseDB" : """Oye {}\n\nPOR ALGUNA RAZÓN NO PUEDES USAR ESTE BOT :(\n\nRAZÓN: {}""",
    "GroupCantUse" : """{} NUNCA ESPERES UNA BUENA RESPUESTA DE MÍ\n
LOS ADMINISTRADORES ME RESTRINGIERON DE TRABAJAR AQUÍ.. 🤭""",
    "GroupCantUseDB" : """{} NUNCA ESPERES UNA BUENA RESPUESTA DE MÍ\n
LOS ADMINISTRADORES ME RESTRINGIERON DE TRABAJAR AQUÍ... 🤭\n\nRAZÓN: {}""",
    "Force": """¡¡Espera [{}](tg://user?id={})..!!\n
Debido al enorme tráfico, solo los miembros del canal pueden usar este bot 🚶\n
¡Esto significa que debe unirse al canal mencionado a continuación para usarme!\n
Presiona `"♻️reintentar♻️"` después de unirte... 😅""",
    "ForceCB": {"🌟 ÚNETE AL CANAL 🌟": "{}", "♻️ Actualizar ♻️": "actualizar"},
    "Fool": "por favor no intentes engañar. 🤭"
}

checkPdf = {
    "pg" : "`Número de páginas: •{}•` 🌟",
    "pdf" : """`¿Qué debo hacer con este archivo?`\n\nNombre del archivo : `{}`\nTamaño del archivo : `{}`""",
    "pdfCB" : {
        "⭐ META£ATA ⭐" : "metaData", "🗳️ VISTA PREVIA 🗳️" : "vista previa",
        "🖼️ IMÁGENES 🖼️" : "pdf|img", "✏️ TEXTO ✏️" : "pdf|txt",
        "🔐 ENCRYPT 🔐" : "work|encrypt", "🔒 DECRYPT 🔓" : "work|decrypt",
        "🗜️ COMPRIMIR 🗜️" : "work|compress", "🤸 GIRAR 🤸" : "pdf|rotate",
        "✂️ SPLIT ✂️" : "pdf|split", "🧬 MERGE 🧬" : "merge", "™️ STAMP ™️" : "pdf|stp",
        "✏️ RENOMBRAR ✏️" : "work|rename", "📝 OCR 📝" : "work|ocr",
         "🥷 FORMATO A4 🥷" : "work|format", "🚫 CERRAR 🚫" : "cerrar|todo"
    },
    "error" : """__No hago nada con este archivo__ 😏\n\n🐉 `CODEC ERROR` 🐉""",
    "errorCB" : {"❌ ERROR EN CODEC ❌" : "error", "🔸 CERRAR 🔸" : "cerrar|todo"},
    "encrypt" : """`EL ARCHIVO ESTÁ CIFRADO` 🔐\n\nNombre del archivo: `{}`\nTamaño del archivo: `{}`""",
    "encryptCB": {"🔓 DECRYPT 🔓": "trabajo|decrypt"}
}

PROGRESS = {
     "progress" : """**\nListo ✅ : **{0}/{1}\n**Velocidad 🚀:** {2}/s\n**Tiempo estimado ⏳:** {3}""",
     "dlImage" : "`Descargando su imagen...⏳`", "upFile" : "`Comenzó a subir...`📤",
     "dlFile" : "`Descargando su archivo..` 📥", "upFileCB" : {"📤 .. CARGANDO.. 📤" : "nabilanavab"},
     "workInP": "TRABAJO EN CURSO... 🙇", "refresh": {"♻️ Actualizar ♻️": "{}"},
     "takeTime" : """```⚙️ Trabajo en progreso..`\n`Puede llevar algo de tiempo..```💛""",
     "cbPRO_D" : ["📤 DESCARGAR: {:.2f}% 📤", "🎯 CANCELAR 🎯"], "cbPRO_U" : ["📤 SUBIDO: {:.2f}% 📤", "🎯 CANCELAR 🎯"]
}

GENERATE = {
     "deleteQueue" : "`Cola eliminada con éxito...`🤧", "noQueue" : "`No se ha encontrado cola...`😲",
     "noImages": "¡¡No se encontró ninguna imagen!! 😒", "getFileNm": "Ahora envíeme un nombre de archivo 😒: ",
     "geting" : "Nombre de archivo: `{}`\nPáginas: `{}`", "getingCB" : {"📚 GENERANDO PDF.." : "nabilanavab"},
     "currDL": "{} Imágenes descargadas 🥱"
}

document = {
    "refresh" : PROGRESS['refresh'], "inWork" : PROGRESS['workInP'], "reply" : checkPdf['pdf'],
    "replyCB" : checkPdf['pdfCB'], "download" : PROGRESS['dlFile'], "process" : "⚙️Procesando..",
    "takeTime" : PROGRESS['takeTime'], "upFile" : PROGRESS['upFile'], "dlImage" : PROGRESS['dlImage'],
    "big" : """Debido a sobrecarga, el propietario limita {}mb para archivos pdf 🙇
\n`por favor envíeme un archivo de menos de {} mb de tamaño` 🙃""",
    "bigCB" : {"💎 Crear bot de soporte de 2 Gb 💎" : "https://github.com/nabilanavab/ilovepdf"},
    "imageAdded" : """`Se agregaron {} página/s a su pdf..`🤓\n\nNombre del archivo: `{}.pdf`""",
    "setHdImg" : """Ahora Image To PDF está en modo HD 😈""",
    "setDefault" : {"« Volver a la calidad predeterminada «" : "close|hd"},
    "error" : """Algo salió mal.. 🐉\n\nERROR: `{}`""",
    "noAPI" : "`Agregue la API de conversión.. 💩\n\ninicio » configuración » api » agregar/cambiar`",
    "useDOCKER" : "`File Not Supported, deploy bot using docker`",
    "fromFile" : "`Convertida: {} to {}`", "unsupport" : "`Archivo no soportado..🙄`",
    "generateRN" : {"GENERAR 📚" : "generate", "REBAUTIZAR ✍️" : "generateREN"},
    "generate" : {"GENERAR 📚" : "generate"}, "cancelCB" : {"⟨ Cancelar ⟩" : "close|me"}
}

noHelp = f"`no one gonna to help you` 😏"

split = {
    "inWork" : PROGRESS['workInP'], "cancelCB" : document['cancelCB'],
    "descargar" : PROGRESS['dlFile'], "exit" : "`Proceso cancelado..` 😏",
    "botón" : {
        "⚙️ PDF » SPLIT ↓" : "nabilanavab", "Con rango 🦞" : "split|R",
        "Página única 🐛" : "split|S", "«BACK«" : "pdf"
    },
    "work" : ["Range", "Single"], "over" : "`5 intentos terminados... Proceso cancelado...`😏",
    "pyromodASK_1" : """__Pdf Split » Por rango\nAhora, ingrese el rango (inicio:fin) :__
\n/salir __para cancelar__""",
    "completed": "`Descarga completada..` ✅",
    "error_1": "`Error de sintaxis: solo es necesario iniciar y finalizar `🚶",
    "error_2": "`Error de sintaxis: errorInEndingPageNumber `🚶",
    "error_3": "`Error de sintaxis: errorInStartingPageNumber `🚶",
    "error_4": "`Error de sintaxis: pageNumberMustBeADigit` 🧠",
    "error_5": "`Error de sintaxis: noEndingPageNumber o notADigit` 🚶",
    "error_6": "`No puedo encontrar ningún número..`😏",
    "error_7" : "`Algo salió mal..`😅", "error_8" : "`Ingrese números menores que {}..`😏",
    "error_9" : "`1st Comprobar número de páginas` 😏", "upload" : "⚙️ `Comenzó a subir...` 📤"
}

pdf2IMG = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "uploadfile" : split["upload"],
    "toImage" : {
        "⚙️ PDF » IMAGES ↓" : "nabilanavab", "🖼 IMG 🖼" : "pdf|img|img",
        "📂 DOC 📂" : "pdf|img|doc", "🤐 ZIP 🤐" : "pdf|img|zip",
        "🎯 TAR 🎯" : "pdf|img|tar","« BACK «" : "pdf" 
    },
    "imgRange" : {
        "⚙️ PDF » IMAGES » {} ↓" : "nabilanavab", "🙄 TODOS 🙄" : "p2img|{}A",
        "🤧 RANGO 🤧" : "p2img|{}R", "🌝 PÁGINAS 🌝" : "p2img|{}S", "« BACK «" : "pdf|img"
    },
    "over" : "`5 intentos terminados... Proceso cancelado..`😏",
    "pyromodASK_1" : """__Pdf - Img›Doc » Páginas:\nAhora, ingrese el rango (inicio:fin) :__
\n/exit __cancelar__""",
    "pyromodASK_2" : """"__Pdf - Imagen›Doc » Páginas:\ahora, ingrese los números de página separados por__ (,) :
\n/exit __cancelar__""",
    "exit" : "`Proceso cancelado..` 😏",
    "error_1" : "`Error de sintaxis: justNeedStartAndEnd `🚶",
    "error_2" : "`Error de sintaxis: errorInEndingPageNumber `🚶",
    "error_3" : "`Error de sintaxis: errorInStartingPageNumber `🚶",
    "error_4" : "`Error de sintaxis: pageNumberMustBeADigit` 🧠",
    "error_5" : "`Error de sintaxis: noEndingPageNumber Or notADigit` 🚶",
    "error_6" : "`No puedo encontrar ningún número..`😏", "error_7" : "`Algo salió mal..`😅",
    "error_8" : "`PDF solo tiene {} páginas` 💩", "error_9" : "`1er Verificación Número de páginas` 😏",
    "error_10" : "__Debido a algunas restricciones, el bot envía solo 50 páginas como ZIP..__😅",
    "total" : "`Paginas totales: {}..⏳`", "upload" : "`Cargando: {}/{} páginas.. 🐬`",
    "current" : "`Convertido: {}/{} páginas.. 🤞`", "complete" : "`Carga completada.. `🏌️",
    "canceledAT" : "`Cancelado en {}/{} páginas..` 🙄", "cbAns" : "⚙️ Okeyda, Canceling.. ",
    "cancelCB" : {"💤 CANCELAR 💤" : "close|P2I"},     # EDITABLE: ❌
    "canceledCB" : {"🍄 CANCELADA 🍄" : "close|P2IDONE"},
    "completed" : {"😎 TERMINADA 😎" : "close|P2ICOMP"}
}

merge = {
     "inWork" : PROGRESS['workInP'], "process" : document['process'], "upload" : PROGRESS['upFile'],
     "load": "__Debido a la sobrecarga, solo puede fusionar 5 archivos PDF a la vez__",
     "sizeLoad": "`Debido a la sobrecarga del bot, solo se admite %sMb pdfs...", # eliminar %s mostrar error
     "pyromodASK" : """__MERGE pdfs » Total de pdfs en cola: {}__

/exit __para cancelar__
/merge __para fusionar__""",
     "exit": "`Proceso cancelado..` 😏", "total": "`Total de PDF: {} 💡",
     "current" : "__Comenzó a descargar PDF : {} 📥__", "cancel" : "`Proceso de fusión cancelado.. 😏`",
     "started" : "__Fusión iniciada.. __ 🪄", "caption" : "`pdf fusionado 🙂`",
     "error": "`Puede ser un archivo cifrado..`\n\nRazón: {}"
}

metaData = {
     "inWork" : PROGRESS['workInP'], "process" : document['process'], "download" : PROGRESS['dlFile'], # [❌]
     "read": "Por favor, lee este mensaje de nuevo... 🥴"
}

preview = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "error" : document['error'],
    "download" : PROGRESS['dlFile'], "_" : "PDF solo tiene {} páginas 🤓\n\n",
    "__" : "Páginas PDF: {}\n\n", "total" : "`Total de páginas: {}..` 🤌",
    "album" : "`Preparando un álbum..` 🤹", "upload" : f"`Cargando: páginas de vista previa.. 🐬`"
}

stamp = {
    "stamp" : {
        "⚙️ PDF » SELLO ↓" : "nabilanavab",
        "No para publicación pública 🤧": "pdf|stp|10",
        "Para publicación pública 🥱": "pdf|stp|8",
        "Confidencial 🤫": "pdf|stp|2", "Departamental 🤝": "pdf|stp|3",
        "Experimental 🔬" : "pdf|stp|4", "Caducado 🐀" : "pdf|stp|5",
        "Final 🔧": "pdf|stp|6", "Para comentarios 🗯️": "pdf|stp|7",
        "No aprobado 😒": "pdf|stp|9", "Aprobado 🥳": "pdf|stp|0",
        "Vendido ✊" : "pdf|stp|11", "Top Secret 😷" : "pdf|stp|12",
        "Borrador 👀" : "pdf|stp|13", "AsIs 🤏" : "pdf|stp|1",
        "« VOLVER «" : "pdf"
    },
    "stampA" : {
        "⚙️ PDF » SELLO » COLOR ↓" : "nabilanavab",
        "Rojo ❤️": "spP|{}|r", "Azul 💙": "spP|{}|b",
        "Verde 💚": "spP|{}|g", "Amarillo 💛": "spP|{}|c1",
        "Rosa 💜": "spP|{}|c2", "Tono 💚": "spP|{}|c3",
        "Blancas 🤍": "spP|{}|c4", "Negras 🖤": "spP|{}|c5",
        "« Volver «" : "pdf|stp"
    },
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "upload" : PROGRESS['upFile'],
    "stamping" : "`Empezó a estampar..` 💠", "caption" : """pdf estampado\ncolor : `{}`\nannot : `{}`"""
}

work = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "takeTime" : PROGRESS['takeTime'],
    "upload" : PROGRESS['upFile'], "botón" : document['cancelCB'],
    "rot360": "Tienes un gran problema...🙂", "ocrError": "Propietario restringido 😎🤏",
    "largeNo" : "enviar un archivo pdf de menos de 5 páginas.. 🙄",
    "pyromodASK_1" : """__PDF {} »\nAhora, ingrese la contraseña:__\n\n/salir __para cancelar__""",
    "pyromodASK_2" : """__Renombrar PDF »\nAhora, ingrese el nuevo nombre:__\n\n/salir __para cancelar__""",
    "exit" : "`proceso cancelado.. `😏", "ren_caption" : "__Nuevo Nombre:__ `{}`",
    "notENCRYPTED" : "`Archivo no cifrado..` 👀",
    "compress" : "⚙️ `Comenzó a comprimir... 🌡️\nPuede llevar algo de tiempo...'💛",
    "decrypt" : "⚙️ `Comenzó a descifrar.. 🔓\nPuede llevar algo de tiempo..`💛",
    "encrypt" : "⚙️ `Comenzó a cifrar.. 🔐\nPuede llevar algo de tiempo..`💛",
    "ocr" : "⚙️ `Agregando capa OCR.. ✍️\nPuede llevar algo de tiempo..`💛",
    "format" : "⚙️ `Comenzó a formatear.. 🤘\nPuede llevar algo de tiempo..`💛",
    "rename" : "⚙️ `Renombrando PDf.. ✏️\nPuede llevar algo de tiempo..`💛",
    "rot" : "⚙️ 'PDF giratorio... 🤸\nPuede que tarde un poco...'💛",
    "pdfTxt": "⚙️ `Extrayendo texto.. 🐾\nPuede llevar algo de tiempo..`💛",
    "fileNm" : "Nombre de archivo antiguo: {}\nNombre de archivo nuevo: {}",
    "rotate" : {
        "⚙️ PDF » ROTETE ↓" : "nabilanavab", "90°" : "work|rot90", "180°" : "work|rot180",
        "270°" : "work|rot270", "360°" : "work|rot360", "« VOLVER «" : "pdf"
    },
    "txt" : {
        "⚙️ PDF » TXT ↓" : "nabilanavab", "📜 MENSAJE 📜" : "work|M", "🧾 TXT FIL 🧾" : "work|T",
        "🌐 HTML 🌐" : "work|H", "🎀 JSON 🎀" : "work|J", "« VOLVER «" : "pdf"
    }
}

PROCESS = {
    "ocr": "OCR agregado", "decryptError": "__No se puede descifrar el archivo con__ `{}` 🕸️",
    "descifrado": "__Archivo descifrado__", "cifrado": "__Número de página__: {}\n__clave__ 🔐: ||{}||",
    "comprimido" : """`Tamaño original : {}\nTamaño comprimido : {}\n\nProporción : {:.2f} %`""",
    "cantCompress": "El archivo no se puede comprimir más...🤐",
    "pgNoError" : """__Por alguna razón FORMATO A4 Admite archivos PDF con menos de 5 páginas__\n\nPáginas totales: {} ⭐""",
    "ocrError": "`Ya tengo una capa de texto... `😏",
    "90" : "__Rotado 90°__", "180" : "__Rotado 180°__", "270" : "__Rotado 270°__",
    "formateado": "Archivo con formato A4", "M": "♻ {} páginas extraídas ♻",
    "H": "Archivo HTML", "T": "Archivo TXT", "J": "Archivo JSON"
}

pdf2TXT = {
    "upload" : PROGRESS["upFile"], "exit" : split['exit'], "nothing" : "Nada que crear... 😏",
    "TEXT": "`Crear PDF a partir de mensajes de texto »`", "start": "Comenzó a convertir txt a Pdf..🎉",
    "font_btn": {
        "TXT@PDF » ESTABLECER FUENTE" : "nabilanavab", "Times" : "pdf|font|t", "Courier" : "pdf|font|c", "Helvetica (predeterminado)" : "pdf|font|h ",
        "Símbolo" : "pdf|font|s", "Zapfdingbats" : "pdf|font|z", "🚫 CLOSE 🚫" : "close|me"
    },
    "size_btn" : { "TXT@PDF » {} » SET SCALE" : "nabilanavab", "Portarate" : "t2p|{}|p", "Landscape" : "t2p|{}|l", "« Volver «": "pdf|T2P"},
    "askT" : "__TEXT TO PDF » Ahora, ingrese un TÍTULO:__\n\n/salir __para cancelar__\n/saltar __para omitir__",
    "askC" : "__TEXT TO PDF » Ahora, ingrese el párrafo {}:__\n\n/salir __para cancelar__\n/crear __para crear__"
}

URL = {
    "get" : {"🧭 Obtener archivo PDF 🧭" : "getFile"}, "close" : HELP_CMD['CB'], "notPDF" : "`No es un archivo PDF",
    "error" : "🐉 ALGO SALIO MAL 🐉\n\nERROR: `{}`\n\nNB: En los grupos, los bots solo pueden buscar documentos enviados después de unirse al grupo =)",
    "done" : "```Casi listo.. ✅\nAhora, comencé a cargar.. 📤```", "_error_" : "envíenme cualquier URL o enlaces directos de telegram pdf",
    "openCB" : {"Abrir en el navegador" : "{}"}, "_error" : "`Algo salió mal =(`\n\n`{}`",
    "_get" : "[Abrir chat]({})\n\n**ACERCA DEL CHAT ↓**\nTipo de chat: {}\nNombre de chat: {}\nUsuario de chat: @{}\n"
             "ID de chat: {}\nFecha: {}\n\n**ACERCA DE MEDIOS ↓**\nMedios: {}\nNombre de archivo: {}\nTamaño de archivo: {}\n\nTipo de archivo: {}"
}

getFILE = {
    "inWork" : PROGRESS['workInP'], "big" : "enviar url de pdf menos de {}mb", "wait" : "Espera... Déjame... 😜",
    "dl" : {"📥 ..DESCARGANDO... 📥" : "nabilanavab"}, "up" : {"📤 ..CARGANDO... 📤" : "nabilanavab"},
    "completed" : {"😎 COMPLETADO 😎" : f"{str(settings.SOURCE_CODE)}"}
}

cbAns = [
    "Esta función está en desarrollo ⛷️", "Error annenn paranjille... entonces qué... 😏",
    "Proceso cancelado.. 😏", "Archivo no cifrado.. 👀", "Nada oficial al respecto.. 😅", "🎉 Completado.. 🏃"
]

inline_query = {
    "TOP" : { "Ahora, seleccione idioma ➟" : "nabilanavab" }, "capt" : "ESTABLECER IDIOMA ⚙️", "des" : "Por: @nabilanavab ❤"
}
