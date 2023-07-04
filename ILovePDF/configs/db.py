# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = os.path.abspath(__file__)


DATA = {}  # save user api, fname, capt

myID = []  # saves bot info if UPDATE_CHANNEL

GROUPS = []  # save groups id and checks each times

invite_link = []  # just saves invitation link

BANNED_USR_DB, BANNED_GRP_DB = [], []  # Load Banned Users Id

CUSTOM_THUMBNAIL_U, CUSTOM_THUMBNAIL_C = [], []  # Load UsersId with custom thumbnail


class dataBASE(object):

    MONGODB_URI = os.environ.get("MONGODB_URI", False)  # mongoDB Url (Optional)


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
