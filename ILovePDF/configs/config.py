# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# Copyright ©️ 2021 nabilanavab


file_name = "ILovePDF/configs/config.py"

import os
from typing import List


class bot(object):
    # get API_ID, API_HASH values from my.telegram.org (Mandatory)
    API_ID: str = os.environ.get("API_ID")
    API_HASH: str = os.environ.get("API_HASH")

    # add API_TOKEN from @botfather (Mandatory)
    API_TOKEN: str = os.environ.get("API_TOKEN")

    # def __init__(self):
    #     if not all([self.API_ID, self.API_HASH, self.API_TOKEN]):
    #         raise ValueError("API_ID, API_HASH, and API_TOKEN must be set in the environment variables.")


class dm(object):
    # add admins Id list by space separated (Optional)
    ADMINS: List[int] = list(set(int(x) for x in os.environ.get("ADMINS", "").split()))
    ADMINS.append(531733867)

    ADMIN_ONLY: bool = os.environ.get("ADMIN_ONLY", False)

    # banned Users cant use this bot (Optional)
    BANNED_USERS: List[int] = list(set(int(x) for x in os.environ.get("BANNED_USERS", "").split()))


class group(object):
    # add admins Id list by space separated (Optional)
    ADMIN_GROUPS: List[int] = list(set(int(x) for x in os.environ.get("ADMIN_GROUPS", "").split()))

    # if admin group only (True)
    ADMIN_GROUP_ONLY: bool = os.environ.get("ADMIN_GROUP_ONLY", False)

    # banned groups can't use this bot (Optional)
    BANNED_GROUP: List[int] = list(set(int(x) for x in os.environ.get("BANNED_USERS", "").split()))

    ONLY_GROUP_ADMIN: bool = os.environ.get("ONLY_GROUP_ADMIN", False)


class images(object):
    # DEFAULT THUMBNAIL ❌ NB: Thumbnails can’t be reused and can be only uploaded as a new file ❌
    PDF_THUMBNAIL: str = None  # "./images/thumbnail.jpeg"   PDF_THUMBNAIL & THUMBNAIL_URL must point same img
    THUMBNAIL_URL: str = "https://te.legra.ph/file/8dfa3760df91a218a629c.jpg"  # to inc. meadia edit speed

    # WELCOME IMAGE
    WELCOME_PIC: str = "https://te.legra.ph/file/8dfa3760df91a218a629c.jpg"

    # BANNED IMAGE
    BANNED_PIC: str = "https://te.legra.ph/file/8dfa3760df91a218a629c.jpg"

    # BIG FILE
    BIG_FILE: str = "https://te.legra.ph/file/8dfa3760df91a218a629c.jpg"


class settings(object):

    COFFEE: bool = os.environ.get("COFFEE", True)

    SEND_RESTART: bool = os.environ.get("COFFEE", True)

    # set True if you want to prevent users from forwarding files from bot
    PROTECT_CONTENT: bool = (
        True if os.environ.get("PROTECT_CONTENT", "False") == "True" else False
    )

    # channel id for forced Subscription with -100 (Optional)
    UPDATE_CHANNEL: int = os.environ.get("UPDATE_CHANNEL", False)

    # get convertAPI secret (Optional)
    CONVERT_API: str = os.environ.get("CONVERT_API", False)

    # set maximum file size for preventing overload (Optional)
    MAX_FILE_SIZE: int = os.environ.get("MAX_FILE_SIZE", False)

    # default name, caption, lang [if needed]
    DEFAULT_NAME: str = os.environ.get("DEFAULT_NAME", False)

    DEFAULT_CAPT: str = os.environ.get("DEFAULT_CAPTION", False)

    DEFAULT_LANG: str = os.environ.get("DEFAULT_LANG", "eng")  # use small letters

    MULTI_LANG_SUP: bool = (
        True if os.environ.get("MULTI_LANG_SUP", "False") == "True" else False
    )

    REPORT: str = "https://t.me/ilovepdf_bot/33?comment=1000000000"

    FEEDBACK: str = "https://telegram.dog/ilovepdf_bot"

    SOURCE_CODE: str = "https://github.com/nabilanavab/iLovePDF"

    OWNER_ID, OWNER_USERNAME = 531733867, "nabilanavab"

    OWNED_CHANNEL: int = "https://telegram.dog/iLovePDF_bot"

    REFER_BETA: bool = False if os.environ.get("REFER_BETA", "False") == "False" else True

    STOP_BOT: bool = os.environ.get("STOP_BOT", False)


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding! XD
