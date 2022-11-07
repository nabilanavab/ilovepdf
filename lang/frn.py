# LANG: FRENCH LANG_CODE: FRN                                      >>  copyright ©️ 2021 nabilanavab  <<                                         fileName : lang/FRN.py
#                                        Thank: nabilanavab                                                   E-mail: nabilanavab@gmail.com

from configs.config import settings

# MESSAGE DE BIENVENUE PM (ACCUEIL A, B, C, D...)
HOME = {
    "HomeA" : """Hey [{}](tg://user?id={})..!!
Ce bot vous aidera à faire beaucoup de choses avec les pdf 🥳

Certaines des fonctionnalités clés sont :\n◍ `Convertir des images en PDF`
◍ `Convertir PDF en images`\n◍ `Convertir fichiers en pdf`""",
    "HomeACB" : {
        "⚙️ PARAMÈTRES ⚙️" : "Home|B", "⚠️ AIDE ⚠️" : "Home|C",
        "📢 CANAL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 CODE SOURCE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🚶 CLOSE 🚶" : "close|mee"
    },
    "HomeAdminCB" : {
        "⚙️ PARAMÈTRES ⚙️" : "Home|B", "⚠️ AIDE ⚠️" : "Home|C",
        "📢 CANAL 📢" : f"{str(settings.OWNED_CHANNEL)}",
        "🌟 CODE SOURCE 🌟" : f"{str(settings.SOURCE_CODE)}",
        "🗽 STATUT 🗽" : f"status|home", "🚶 CLOSE 🚶" : "close|mee"
    },
    "HomeB" : """PAGE DES PARAMÈTRES ⚙️\n\nNOM D'UTILISATEUR : {}
ID D'UTILISATEUR : {}\nNOM D'UTILISATEUR : {}\nDATE D'INSCRIPTION : {}\n
LANGUE : {}\nAPI : {}
POUCE : {}\nCAPTION : {}\nNOM DU FICHIER : {}""",
    "HomeBCB" : {
        "🌍 LANG 🌍" : "set|lang", "📍 POUCE 📍" : "set|thumb",
        "📈 NOM 📈" : "set|fname", "💩 API 💩" : "set|api",
        "📅 CAPTION 📅" : "set|capt", "« RETOUR À L'ACCUEIL »" : "Home|B2A"
    },
    "HomeC" : """🪂 **MESSAGE D'AIDE** 🪂 :

```Certaines des fonctionnalités principales sont :
 ◍ Convertir des images en PDF\n ◍ Manupultions PDF\n ◍ De nombreux codecs populaires en pdf
 
Modifier le fichier pdf :
 ◍ PDF⥃IMAGES [all,range,pages]\n ◍ DOCS to PDF [png, jpg, jpeg]\n ◍ IMAGES⥃PDF\n ◍ PDF METADATA\n ◍ PDF⥃TEXT\n ◍ TEXT⥃PDF\n ◍ Compresser le fichier pdf
 ◍ SPLIT PDF [plage, pages]\n ◍ FUSIONNER PDF\n ◍ AJOUTER UN TAMPON\n ◍ RENOMMER PDF\n ◍ ROTATION PDF\n ◍ CRYPTAGE/DÉCRYPTAGE PDF\n ◍ FORMATEUR PDF \n ◍ PDF⥃JSON/TXT FILE
 ◍ PDF⥃HTML [vue Web]\n ◍ URL⥃PDF\n ◍ PDF⥃ZIP/TAR/RAR [tout, plage, pages]\nEt bien plus encore... ```""",
    "HomeCCB" : {"« RETOUR À L'ACCUEIL " : "Home|A", "🛈 CONSIGNES 🛈" : "Home|D"},
    "HomeD" : """`Comme il s'agit d'un service gratuit, je ne peux pas garantir combien de temps je pourrai maintenir ce service..`😝
 
⚠️CONSIGNES⚠️ :
🛈 __S'il vous plaît, n'essayez pas d'abuser de Bot Admins__ 😒
🛈 __Ne spammez pas ici, cela pourrait entraîner un bannissement permanent 🎲__.
🛈 __Le contenu porno vous donnera également une BAN PERMANENTE 💯__

**Envoyez n'importe quelle image pour commencer :** 😁""",
    "HomeDCB" : {"⚠️ AIDE ⚠️" : "Home|C", "» RETOUR ACCUEIL »" : "Home|A"}
}

SETTINGS = {
    "default" : ["DEFAULT ❌", "CUSTOM ✅"], "chgLang" : {"SETTING ⚙️ » CHANGE LANG 🌐" : "nabilanavab"},
    "error" : "Une erreur s'est produite lors de la récupération des données de la base de données", "lang" : "Maintenant, sélectionnez une langue..",
    "ask" : ["Maintenant, envoie-moi..", "Maintenant, envoie-moi.. 😅\n\nVite. ! Je n'ai plus le temps de relire le texte.. 😏\n\n/cancel : pour annuler "],
    "askApi" : "\n\nOuvrez le lien ci-dessous et envoyez-moi le code secret :", "waitApi" : {"Ouvrir le lien ✅" : "https://www.convertapi.com/a/signin"},
    "wait" : {"Attente.. 🥱" : "nabilanavab"}, "back" : {"« RETOUR À L'ACCUEIL »" : "Home|B2S"}, "errorCB" : {"« RETOUR À L'ACCUEIL «" : "Home|B2A"},
    "result" : ["Les paramètres ne peuvent pas être mis à jour ❌", "Les paramètres ont été mis à jour avec succès ✅"], "cant" : "Cette fonctionnalité ne peut pas être utilisée ❌",
    "feedback" : "Avis de clients géniaux comme vous aidez les autres.\n@nabilanavab"
                 "\n\nSignaler un BUG en {} Lang :\n`• Spécifiez la Lang\n• Message d'erreur\n• Nouveau message`",
    "feedbtn" : {"Signaler une erreur de langue" : settings.REPORT},
    "thumb" : [
        {"SETTING ⚙️ » THUMBNAIL 📷" : "nabilanavab", "♻ ADD ♻" : "set|thumb+", "« RETOUR À L'ACCUEIL »": "Home|B"},
        {"SETTING ⚙️ » THUMBNAIL 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|thumb+", "🗑 DELETE 🗑" : "set|thumb-", "« BACK TO HOME »" : "Home|B2S"}
    ],
    "fname" : [
        {"SETTING ⚙️ » FNAME 📷" : "nabilanavab", "♻ ADD ♻" : "set|fname+", "« RETOUR À L'ACCUEIL »" : "Home|B2S"},
        {"SETTING ⚙️ » FNAME 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|fname+", "🗑 DELETE 🗑" : "set|fname-", "« BACK TO HOME »" : "Home|B2S"}
    ],
    "api" : [
        {"SETTING ⚙️ » API 📷" : "nabilanavab", "♻ ADD ♻" : "set|api+", "« RETOUR À L'ACCUEIL »" : "Home|B2S"},
        {"SETTING ⚙️ » API 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|api+", "🗑 DELETE 🗑" : "set|api-", "« RETOUR À L'ACCUEIL »" : "Home|B2S"}
    ],
    "capt" : [
        {"RÉGLAGE ⚙️ » LÉGENDE 📷" : "nabilanavab", "♻ AJOUTER ♻" : "set|capt+", "« RETOUR À L'ACCUEIL »" : "Home|B2S"},
        {"SETTING ⚙️ » CAPTION 📷" : "nabilanavab", "♻ CHANGE ♻" : "set|capt+", "🗑 SUPPRIMER 🗑" : "set|capt-", "« RETOUR À L'ACCUEIL »" : "Home|B2S"}
    ]
}

BOT_COMMAND = {"start" : "Message de bienvenue..", "txt2pdf" : "Créer des PDF texte"}

HELP_CMD = {
    "userHELP" : """[MESSAGES DE COMMANDE UTILISATEUR] :\n
/start : pour vérifier si le bot est actif\n/cancel : annuler le travail en cours
/delete : effacer l'image dans la file d'attente pdf\n/txt2pdf : texte en pdf""",
    "adminHelp" : """\n\n\n[MESSAGES DE COMMANDE ADMIN] :\n
/send : pour diffuser, message pm""",
    "footerHelp" : f"""\n\n\nCode source : [i 💜 PDF]({str(settings.SOURCE_CODE)})
Bot : @complete_pdf_bot 💎\n[Canal d'assistance]({settings.OWNED_CHANNEL})""",
    "CB" : {"⚠️ FERMER ⚠️" : "fermer|tous"}
}

STATUS_MSG = {
    "HOME" : "`Maintenant, sélectionnez l'une des options ci-dessous pour obtenir l'état actuel 💱.. `",
    "_HOME" : {
        "📊 ↓ SERVEUR ↓ 📊" : "nabilanavab", "📶 STOCKAGE 📶" : "état|serveur",
        "🥥 DATABASE 🥥" : "status|db", "🌝 ↓ GET LIST ↓ 🌝": "nabilanavab",
        "💎 ADMIN 💎" : "état|admin", "👤 UTILISATEURS 👤" : "état|utilisateurs",
        "« RETOUR «" : "Accueil|A"
    },
    "DB" : """📂 BASE DE DONNÉES :\n\n**◍ Utilisateurs de la base de données :** `{}` 📍\n**◍ Chats de la base de données :** `{}` 📍""",
    "SERVER" : """**◍ Espace total :** `{}`
**◍ Espace utilisé :** `{}({}%)`\n**◍ Espace libre :** `{}`
**◍ Utilisation CPU :** `{}`%\n**◍ Utilisation RAM :** `{}`%
**◍ Travail en cours :** `{}`\n**◍ Identifiant du message :** `{}`""",
    "BACK" : {"« RETOUR «" : "état|accueil"}, "ADMIN" : "**Total ADMIN :** __{}__\n",
    "USERS" : "Les utilisateurs enregistrés dans la base de données sont :\n\n", "NO_DB" : "Aucune base de données définie pour le moment 💩"
}

feedbackMsg = f"[Ecrire un commentaire 📋]({settings.FEEDBACK})"

# MESSAGE DE BIENVENUE AU GROUPE
HomeG = {
    "HomeA" : """Bonjour. ! 🖐️\nJe suis nouveau ici {message.chat.title}\n
Permettez-moi de me présenter..\nMon nom est iLovePDF, et je peux vous aider à faire beaucoup
Choses avec les fichiers PDF @Telegram\n\nMerci @nabilanavab pour ce robot génial 😅""",
    "HomeACB" : {
        "🤠 PROPRIÉTAIRE DU BOT 🤠": f"https://telegram.dog/{settings.OWNER_USERNAME}",
        "🛡️ METTRE À JOUR LE CANAL 🛡️": f"{settings.OWNED_CHANNEL}", "🌟 CODE SOURCE 🌟": f"{settings.SOURCE_CODE}"
    }
}

# UI UTILISATEUR INTERDIT
BAN = {
    "cbNotU" : "Message pas pour toi.. 😏",
    "banCB" : {
        "Créez votre propre bot": f"{settings.SOURCE_CODE}", "Tutoriel": f"{settings.SOURCE_CODE}",
        "Chaîne de mise à jour": "https://telegram.dog/ilovepdf_bot"
    },
    "UCantUse" : """Hey {}\n\nPOUR QUELQUE RAISON QUE VOUS NE POUVEZ PAS UTILISER CE BOT :(""",
    "UCantUseDB" : """Hé {}\n\nPOUR QUELQUE RAISON QUE VOUS NE POUVEZ PAS UTILISER CE BOT :(\n\nRAISON : {}""",
    "GroupCantUse" : """{} N'ATTENDEZ JAMAIS UNE BONNE RÉPONSE DE MOI\n
LES ADMINS M'ONT RESTREINT DE TRAVAILLER ICI .. 🤭""",
    "GroupCantUseDB" : """{} N'ATTENDEZ JAMAIS UNE BONNE RÉPONSE DE MOI\n
LES ADMINS M'ONT INTERDIT DE TRAVAILLER ICI. 🤭\n\nRAISON : {}""",
    "Force" : """Attendez [{}](tg://user?id={})..!!\n
En raison de l'énorme trafic, seuls les membres de la chaîne peuvent utiliser ce bot 🚶\n
Cela signifie que vous devez rejoindre la chaîne mentionnée ci-dessous pour m'utiliser !\n
Appuyez sur `"♻️réessayer♻️"` après avoir rejoint.. 😅""",
    "ForceCB" : {"🌟 REJOINDRE LE CANAL 🌟" : "{}", "♻️ Actualiser ♻️" : "refresh"},
    "Fool" : "tu ne peux pas me tromper.. 🤭"
}

checkPdf = {
    "pg" : "`Nombre de pages : •{}•` 🌟",
    "pdf" : """`Que dois-je faire avec ce fichier ?`\n\nNom du fichier : `{}`\nTaille du fichier : `{}`""",
    "pdfCB" : {
        "⭐ META£ATA ⭐" : "metaData", "🗳️ APERÇU 🗳️" : "preview",
        "🖼️ IMAGES 🖼️" : "pdf|img", "✏️ TEXTE ✏️" : "pdf|txt",
        "🔐 ENCRYPT 🔐" : "work|encrypt", "🔒 DECRYPT 🔓" : "work|decrypt",
        "🗜️ COMPRESSER 🗜️" : "work|compresser", "🤸 ROTATION 🤸" : "pdf|rotate",
        "✂️ SPLIT ✂️" : "pdf|split", "🧬 MERGE 🧬" : "merge", "™️ STAMP ™️" : "pdf|stp",
        "✏️ RENOMMER ✏️" : "work|rename", "📝OCR 📝" : "work|ocr",
         "🥷 FORMAT A4 🥷" : "work|format", "🚫 FERMER 🚫" : "close|all"
    },
    "error" : """__Je ne fais rien avec ce fichier__ 😏\n\n🐉 `CODEC ERROR` 🐉""",
    "errorCB" : {"❌ ERREUR DANS LE CODEC ❌" : "error", "🔸 CLOSE 🔸" : "close|all"},
    "encrypt" : """`LE FICHIER EST CRYPTÉ` 🔐\n\nNom du fichier : `{}`\nTaille du fichier : `{}`""",
    "encryptCB" : {"🔓 DECRYPTER 🔓" : "work|decrypt"}
}

PROGRESS = {
    "progress" : """**\nTerminé ✅ : **{0}/{1}\n**Vitesse 🚀 :** {2}/s\n**Temps estimé ⏳ :** {3}""",
    "dlImage" : "`Téléchargement de votre image..⏳`", "upFile" : "`Téléchargement en cours..`📤",
    "dlFile" : "`Téléchargement de votre fichier..` 📥", "upFileCB" : {"📤 .. UPLOADING.. 📤" : "nabilanavab"},
    "workInP" : "TRAVAIL EN COURS.. 🙇", "refresh" : {"♻️ Refresh ♻️" : "{}"},
    "takeTime" : """```⚙️ Travail en cours..`\n`Cela peut prendre un certain temps..```💛""",
    "cbPRO_D" : ["📤 TÉLÉCHARGEMENT : {:.2f}% 📤", "🎯 ANNULER 🎯"], "cbPRO_U" : ["📤 TÉLÉCHARGEMENT : {:.2f}% 📤", "🎯 ANNULER 🎯"]
}

GENERATE = {
    "deleteQueue" : "`File d'attente supprimée avec succès..`🤧", "noQueue" : "`Aucune file d'attente fondée..`😲",
    "noImages" : "Aucune image trouvée.!! 😒", "getFileNm" : "Envoyez-moi maintenant un nom de fichier 😒 : ",
    "geting" : "Nom du fichier : `{}`\nPages : `{}`", "getingCB" : {"📚 GÉNÉRER UN PDF.." : "nabilanavab"},
    "currDL" : "Images {} téléchargées 🥱"
}

document = {
    "refresh" : PROGRESS['refresh'], "inWork" : PROGRESS['workInP'], "reply" : checkPdf['pdf'],
    "replyCB" : checkPdf['pdfCB'], "download" : PROGRESS['dlFile'], "process" : "⚙️ Traitement..",
    "takeTime" : PROGRESS['takeTime'], "upFile" : PROGRESS['upFile'], "dlImage" : PROGRESS['dlImage'],
    "big" : """ En raison d'une surcharge, le propriétaire limite {} Mo pour les fichiers pdf 🙇
\n`s'il vous plaît envoyez-moi un fichier de moins de {}mb Size` 🙃""",
    "bigCB" : {"💎 Créer un robot de support 2Gb 💎" : "https://github.com/nabilanavab/ilovepdf"},
    "imageAdded" : """`Ajouté {} page/s à votre pdf..`🤓\n\nfileName : `{}.pdf`""",
    "setHdImg" : """Maintenant Image To PDF est en mode HD 😈""",
    "setDefault" : {"« Retour à la qualité par défaut «" : "close|hd"},
    "error" : """QUELQUE CHOSE s'est mal passé.. 🐉\n\nERREUR : `{}`""",
    "noAPI" : "`Veuillez ajouter l'API de conversion.. 💩\n\ndémarrer » paramètres » api » ajouter/modifier`",
    "useDOCKER" : "`Fichier non pris en charge, déployer le bot à l'aide de docker`",
    "fromFile" : "`Converti : {} en {}`", "unsupport" : "`fichier non pris en charge..🙄`",
    "generateRN" : {"GENERATE 📚" : "generate", "RENAME ✍️" : "generateREN"},
    "generate" : {"GENERATE 📚" : "generate"}, "cancelCB" : {"⟨ Cancel ⟩" : "close|me"}
}

noHelp = f"`personne ne va vous aider` 😏"

split = {
    "inWork" : PROGRESS['workInP'], "cancelCB" : document['cancelCB'],
    "download" : PROGRESS['dlFile'], "exit" : "`Processus annulé..` 😏",
    "bouton" : {
        "⚙️ PDF » SPLIT ↓" : "nabilanavab", "With In Range 🦞" : "split|R",
        "Page unique 🐛" : "split|S", "« RETOUR «" : "pdf"
    },
    "work" : ["Range", "Single"], "over" : "`5 tentatives terminées.. Processus annulé..`😏",
    "pyromodASK_1" : """__Pdf Split » By Range\nMaintenant, entrez la plage (début:fin) :__
\n/quitter __pour annuler__""",
    "completed" : "`Téléchargement terminé..` ✅",
    "error_1" : "`Erreur de syntaxe : justNeedStartAndEnd `🚶",
    "error_2" : "`Erreur de syntaxe : errorInEndingPageNumber `🚶",
    "error_3" : "`Erreur de syntaxe : errorInStartingPageNumber `🚶",
    "error_4" : "`Erreur de syntaxe : numéro de page doit être un chiffre` 🧠",
    "error_5" : "`Erreur de syntaxe : noEndingPageNumber ou notADigit` 🚶",
    "error_6" : "`Je ne trouve aucun numéro..`😏",
    "error_7" : "`Quelque chose s'est mal passé..`😅", "error_8" : "`Entrez des nombres inférieurs à {}..`😏",
    "error_9" : "`1ère vérification du nombre de pages` 😏", "upload" : "⚙️ `Téléchargement commencé..` 📤"
}

pdf2IMG = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "uploadfile" : split["upload"],
    "toImage" : {
        "⚙️ PDF » IMAGES ↓" : "nabilanavab", "🖼 IMG 🖼" : "pdf|img|img",
        "📂 DOC 📂" : "pdf|img|doc", "🤐 ZIP 🤐" : "pdf|img|zip",
        "🎯 TAR 🎯" : "pdf|img|tar","« RETOUR «" : "pdf"
    },
    "imgRange" : {
        "⚙️ PDF » IMAGES » {} ↓" : "nabilanavab", "🙄 TOUS 🙄" : "p2img|{}A",
        "🤧 GAMME 🤧" : "p2img|{}R", "🌝 PAGES 🌝" : "p2img|{}S", "« RETOUR «" : "pdf|img"
    },
    "over" : "`5 tentatives terminées.. Processus annulé..`😏",
    "pyromodASK_1" : """__Pdf - Img›Doc » Pages :\nMaintenant, entrez la plage (début:fin) :__
\n/quitter __pour annuler__""",
    "pyromodASK_2" : """"__Pdf - Img›Doc » Pages :\nMaintenant, entrez les numéros de page séparés par__ (,) :
\n/quitter __pour annuler__""",
    "exit" : "`Processus annulé..` 😏",
    "error_1" : "`Erreur de syntaxe : justNeedStartAndEnd `🚶",
    "error_2" : "`Erreur de syntaxe : errorInEndingPageNumber `🚶",
    "error_3" : "`Erreur de syntaxe : errorInStartingPageNumber `🚶",
    "error_4" : "`Erreur de syntaxe : numéro de page doit être un chiffre` 🧠",
    "error_5" : "`Erreur de syntaxe : noEndingPageNumber ou notADigit` 🚶",
    "error_6" : "`Je ne trouve aucun numéro..`😏", "error_7" : "`Quelque chose s'est mal passé..`😅",
    "error_8" : "`Le PDF n'a que {} pages` 💩", "error_9" : "`1er vérifier le nombre de pages` 😏",
    "error_10" : "__En raison de certaines restrictions, le bot n'envoie que 50 pages au format ZIP..__😅",
    "total" : "`Total pages : {}..⏳`", "upload" : "`Téléchargement : {}/{} pages.. 🐬`",
    "current" : "`Conversion : {}/{} pages.. 🤞`", "complete" : "`Téléchargement terminé.. `🏌️",
    "canceledAT" : "`Annulé à {}/{} pages..` 🙄", "cbAns" : "⚙️ Okeyda, Annulation.. ",
    "annulerCB" : {"💤 ANNULER 💤" : "fermer|P2I"}, # MODIFIABLE : ❌
    "canceledCB" : {"🍄 CANCELED 🍄" : "close|P2IDONE"},
    "completed" : {"😎 TERMINÉ 😎" : "fermer|P2ICOMP"}
}

merge = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'], "upload" : PROGRESS['upFile'],
    "load" : "__En raison de la surcharge, vous ne pouvez fusionner que 5 pdf à la fois__",
    "sizeLoad": "` En raison de la surcharge du bot, seuls %sMb pdfs sont pris en charge..", # suppression de %s show error
    "pyromodASK" : """__MERGE pdfs » Nombre total de pdf dans la file d'attente : {}__

/quitter __pour annuler__
/merge __pour fusionner__""",
    "exit" : "`Processus annulé..` 😏", "total" : "`Total PDF's : {} 💡",
    "current" : "__Started Downloading Pdf : {} 📥__", "cancel" : "`Merge Process Cancelled.. 😏`",
    "started" : "__Merging Started.. __ 🪄", "caption" : "`merged pdf 🙂`",
    "error" : "`Peut être un fichier crypté..`\n\nRaison : {}"
}

metaData = {
     "inWork" : PROGRESS['workInP'], "process" : document['process'], "download" : PROGRESS['dlFile'], # [❌]
     "read" : "Merci de relire ce message.. 🥴"
}

preview = {
     "inWork" : PROGRESS['workInP'], "process" : document['process'], "error" : document['error'],
     "download" : PROGRESS['dlFile'], "_" : "Le PDF n'a que {} pages 🤓\n\n",
     "__" : "Pages PDF : {}\n\n", "total" : "`Nombre total de pages : {}..` 🤌",
     "album" : "`Préparation d'un album..` 🤹", "upload" : f"`Téléchargement : pages d'aperçu.. 🐬`"
}

stamp = {
    "stamp" : {
        "⚙️ PDF » TIMBRE ↓" : "nabilanavab",
        "Pas pour diffusion publique 🤧" : "pdf|stp|10",
        "Pour diffusion publique 🥱" : "pdf|stp|8",
        "Confidentiel 🤫" : "pdf|stp|2", "Départemental 🤝" : "pdf|stp|3",
        "Expérimental 🔬" : "pdf|stp|4", "Expiré 🐀" : "pdf|stp|5",
        "Finale 🔧" : "pdf|stp|6", "Pour un commentaire 🗯️" : "pdf|stp|7",
        "Non approuvé 😒" : "pdf|stp|9", "Approuvé 🥳" : "pdf|stp|0",
        "Vendu ✊" : "pdf|stp|11", "Top secret 😷" : "pdf|stp|12",
        "Brouillon 👀" : "pdf|stp|13", "Tel quel 🤏" : "pdf|stp|1",
        "« RETOUR «" : "pdf"
    },
    "stampA" : {
        "⚙️ PDF » TAMPON » COULEUR ↓" : "nabilanavab",
        "Rouge ❤️" : "spP|{}|r", "Bleu 💙" : "spP|{}|b",
        "Vert 💚" : "spP|{}|g", "Jaune 💛" : "spP|{}|c1",
        "Rose 💜" : "spP|{}|c2", "Teinte 💚" : "spP|{}|c3",
        "Blanc 🤍" : "spP|{}|c4", "Noir 🖤" : "spP|{}|c5",
        "« Retour «" : "pdf|stp"
    },
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "download" : PROGRESS['dlFile'], "upload" : PROGRESS['upFile'],
    "stamping" : "`Started Stamping..` 💠", "caption" : """pdf tamponné\ncouleur : `{}`\nannot : `{}`"""
}

work = {
    "inWork" : PROGRESS['workInP'], "process" : document['process'],
    "télécharger" : PROGRESS['dlFile'], "takeTime" : PROGRESS['takeTime'],
    "upload" : PROGRESS['upFile'], "button" : document['cancelCB'],
    "rot360" : "Vous avez un gros problème..🙂", "ocrError" : "Propriétaire restreint 😎🤏",
    "largeNo" : "envoyer un fichier pdf de moins de 5 pages.. 🙄",
    "pyromodASK_1" : """__PDF {} »\nMaintenant, veuillez saisir le mot de passe :__\n\n/exit __pour annuler__""",
    "pyromodASK_2" : """__Renommer le PDF »\nMaintenant, veuillez saisir le nouveau nom :__\n\n/quitter __pour annuler__""",
    "exit" : "`processus annulé.. `😏", "ren_caption" : "__Nouveau nom :__ `{}`",
    "notENCRYPTED" : "`Fichier non crypté..` 👀",
    "compress" : "⚙️ `Compression commencée.. 🌡️\nCela peut prendre un certain temps..`💛",
    "decrypt" : "⚙️ `Décryptage commencé.. 🔓\nCela peut prendre un certain temps..`💛",
    "encrypt" : "⚙️ `Cryptage commencé.. 🔐\nCela peut prendre un certain temps..`💛",
    "ocr" : "⚙️ `Ajout d'une couche OCR.. ✍️\nCela peut prendre un certain temps..`💛",
    "format" : "⚙️ `Formatage commencé.. 🤘\nCela peut prendre un certain temps..`💛",
    "rename" : "⚙️ `Renommer le PDf.. ✏️\nCela peut prendre un certain temps..`💛",
    "rot" : "⚙️ `Rotation PDf.. 🤸\nCela peut prendre un certain temps..`💛",
    "pdfTxt" : "⚙️ `Extraire du texte.. 🐾\nCela peut prendre un certain temps..`💛",
    "fileNm" : "Ancien nom de fichier : {}\nNouveau nom de fichier : {}",
    "rotate" : {
        "⚙️ PDF » ROTETE ↓" : "nabilanavab", "90°" : "work|rot90", "180°" : "work|rot180",
        "270°" : "work|rot270", "360°" : "work|rot360", "« RETOUR «" : "pdf"
    },
    "TXT" : {
        "⚙️ PDF » TXT ↓" : "nabilanavab", "📜 MESSAGE 📜" : "work|M", "🧾 TXT FIL 🧾" : "work|T",
        "🌐 HTML 🌐" : "work|H", "🎀 JSON 🎀" : "work|J", "« RETOUR «" : "pdf"
    }
}

PROCESS = {
    "ocr" : "OCR ajouté", "decryptError" : "__Impossible de déchiffrer le fichier avec__ `{}` 🕸️",
    "decrypted" : "__Decrypted File__", "encrypted" : "__Page Number__ : {}\n__key__ 🔐 : ||{}||",
    "compressed" : """`Taille d'origine : {}\nTaille compressée : {}\n\nRatio : {:.2f} %`""",
    "cantCompress" : "Le fichier ne peut plus être compressé..🤐",
    "pgNoError" : """__For Some Reason A4 FORMATTING Supports for pdfs with under than 5 Pages__\n\nTotal Pages: {} ⭐""",
    "ocrError" : "`A déjà un calque de texte.. `😏",
    "90" : "__Rotated 90°__", "180" : "__Rotated 180°__", "270" : "__Rotated 270°__",
    "formatted" : "Fichier au format A4", "M" : "♻ Pages {} extraites ♻",
    "H" : "Fichier HTML", "T" : "Fichier TXT", "J" : "Fichier JSON"
}

pdf2TXT = {
    "upload" : PROGRESS["upFile"], "exit" : split['exit'], "nothing" : "Rien à créer.. 😏",
    "TEXT" : "`Créer un PDF à partir de messages texte »`", "start" : "Démarrage de la conversion de txt en Pdf..🎉",
    "font_btn" : {
        "TXT@PDF » SET FONT" : "nabilanavab", "Times" : "pdf|font|t", "Courier" : "pdf|font|c", "Helvetica (Default)" : "pdf|font|h ",
        "Symbol" : "pdf|font|s", "Zapfdingbats" : "pdf|font|z", "🚫 CLOSE 🚫" : "close|me"
    },
    "size_btn" : { "TXT@PDF » {} » SET SCALE" : "nabilanavab", "Portarate" : "t2p|{}|p", "Landscape" : "t2p|{}|l", "« Retour «": "pdf|T2P"},
    "askT" : "__TEXT TO PDF » Maintenant, veuillez saisir un TITLE :__\n\n/exit __to cancel__\n/skip __to skip__",
    "askC" : "__TEXT TO PDF » Maintenant, veuillez saisir le paragraphe {} :__\n\n/exit __pour annuler__\n/create __pour créer__"
}

URL = {
    "get" : {"🧭 Obtenir un fichier PDF 🧭" : "getFile"}, "close" : HELP_CMD['CB'], "notPDF" : "`Pas un fichier PDF",
    "error" : "🐉 QUELQUE CHOSE S'EST TROMPÉ 🐉\n\nERREUR : `{}`\n\nNB : Dans les groupes, les bots ne peuvent récupérer que les documents envoyés après avoir rejoint le groupe =)",
    "done" : "```Presque terminé.. ✅\nMaintenant, le téléchargement a commencé.. 📤```", "_error_" : "envoyez-moi des URL ou des liens pdf directs vers des télégrammes",
    "openCB" : {"Ouvrir dans le navigateur" : "{}"}, "_error" : "`Quelque chose s'est mal passé =(`\n\n`{}`",
    "_get" : "[Ouvrir le chat]({})\n\n**À PROPOS DU CHAT ↓**\nType de chat : {}\nNom du chat : {}\nChat Usr : @{}\n"
             "ID de chat : {}\nDate : {}\n\n**À PROPOS DES MÉDIAS ↓**\nMédia : {}\nNom du fichier : {}\nTaille du fichier : {}\n\nType de fichier : {}"
}

getFILE = {
    "inWork" : PROGRESS['workInP'], "big" : "envoyer une URL pdf inférieure à {}mb", "wait" : "Attendez.. Laissez-moi.. 😜",
    "dl" : {"📥 ..TÉLÉCHARGEMENT.. 📥" : "nabilanavab"}, "up" : {"📤 ..TÉLÉCHARGEMENT.. 📤" : "nabilanavab"},
    "complet" : {"😎 TERMINÉ 😎" : f"{str(settings.SOURCE_CODE)}"}
}

cbAns = [
    "Cette fonctionnalité est en cours de développement ⛷️", "Erreur annenn paranjille.. alors quoi.. 😏",
    "Processus annulé.. 😏", "Fichier non crypté.. 👀", "Rien d'officiel à ce sujet.. 😅", "🎉 Terminé.. 🏃"
]

inline_query = {
    "TOP" : { "Maintenant, sélectionnez la langue ➟" : "nabilanavab" }, "capt" : "SET LANGUAGE ⚙️", "des" : "Par : @nabilanavab ❤"
}

# ===================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
