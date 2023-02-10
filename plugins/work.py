# fileName : plugins/work.py
# copyright ©️ 2021 nabilanavab

import os, shutil
from pyrogram import enums

async def work(message, work="check", mtype=True) -> "str":
    """
    create a new working dir
    mtype: TRUE if message or FALSE if callbackquery
    work: create, check, delete
    """
    if mtype:
        if message.chat.type == enums.ChatType.PRIVATE:
            path = f"work/nabilanavab/{message.chat.id}"
        else:
            pat = f"work/nabilanavab/{message.chat.id}"
            path = f"work/nabilanavab/{message.chat.id}/{message.from_user.id}"
    else:
        if message.message is None:
            # inline query download cant get message from callback
            path = f"work/nabilanavab/inline{message.data.split('|')[2]}"
        elif message.message.chat.type == enums.ChatType.PRIVATE:
            path = f"work/nabilanavab/{message.message.chat.id}"
        else:
            pat = f"work/nabilanavab/{message.message.chat.id}"
            path = f"work/nabilanavab/{message.message.chat.id}/{message.message.from_user.id}"
    if work == "create":
        if os.path.exists(path):
            return False    # False if work exists
        os.makedirs(path)
        return path
    elif work == "check":
        return path if os.path.exists(path) else False
    elif work == "delete":
        if mtype and message.chat.type != enums.ChatType.PRIVATE and len(os.listdir(pat)) == 1:
            return shutil.rmtree(pat, ignore_errors=True)
        elif not mtype and message.message is None:
            # inline message
            return shutil.rmtree(path, ignore_errors=True)
        elif not mtype and message.message.chat.type != enums.ChatType.PRIVATE and len(os.listdir(pat)) == 1:
            return shutil.rmtree(pat, ignore_errors=True)
        return shutil.rmtree(path, ignore_errors=True)
