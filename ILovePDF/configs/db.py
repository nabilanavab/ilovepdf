# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# Copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/configs/db.py"

import os

# Save user API, first name, caption
DATA = {}

# Saves bot info if UPDATE_CHANNEL
myID = []

# Save groups ID and check each time
GROUPS = []

# Save users who need notification after bot restarts from stop
ping_list = []

# Save invitation links
invite_link = []

# Load Banned Users ID
BANNED_USR_DB, BANNED_GRP_DB = [], []

# Load Users ID with custom thumbnail
CUSTOM_THUMBNAIL_U, CUSTOM_THUMBNAIL_C = [], []

# MongoDB URL (Optional)
class dataBASE:
    MONGODB_URI = os.environ.get("MONGODB_URI", False)


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better. Happy coding! XD
