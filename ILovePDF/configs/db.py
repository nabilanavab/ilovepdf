# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# Copyright ©️ 2021 nabilanavab


file_name = "ILovePDF/configs/db.py"

import os
from typing import List

# Save user API, first name, caption
DATA: dict = {}

# Saves bot info if UPDATE_CHANNEL
myID: List = []

# Save groups ID and check each time
GROUPS: List[int] = []

# Save users who need notification after bot restarts from stop
ping_list: List[int] = []

# Save invitation links
invite_link: List[str] = []

# Load Banned Users ID
BANNED_USR_DB: List[int] = []
BANNED_GRP_DB: List[int] = []

# Load Users ID with custom thumbnail
CUSTOM_THUMBNAIL_U: List[int] = []
CUSTOM_THUMBNAIL_C: List[int] = []

# MongoDB URL (Optional)
class dataBASE:
    MONGODB_URI: str = os.environ.get("MONGODB_URI", False)


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better. Happy coding! XD