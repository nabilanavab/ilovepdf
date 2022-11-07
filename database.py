# fileName : database.py
# copyright ©️ 2021 nabilanavab

# pip install motor
import datetime
import motor.motor_asyncio
from configs.db import dataBASE
from configs.config import settings

class Database:
    # CONSTRUCTORS (__init__)
    def __init__(self, uri, database_name):
        # CREATING A SINGLE INSTANCE
        self._client=motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db=self._client[database_name]
        # clusters [users, group]
        self.col=self.db.users
        self.grp=self.db.groups
    
    #ADD NEW USER TO DB
    def new_user(self, id, name, lang_code):
        if lang_code != settings.DEFAULT_LANG:
            return dict(id = id, name = name, join_date = datetime.date.today().isoformat(), lang = lang_code)
        return dict(id = id, name = name, join_date = datetime.date.today().isoformat())
    
    #ADD NEW GROUP TO DB
    def new_group(self, id, title):
        return dict(id = id, title = title, join_date = datetime.date.today().isoformat())
    
    # -------------------------------- CHECK IF USER/GROUP EXIST -------------------------------------
    # [user]
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)
    # [group]
    async def is_chat_exist(self, chat):
        chat = await self.grp.find_one({'id': int(chat)})
        return bool(chat)
    
    # ----------------------------------- ADD NEW USER/GROUP -----------------------------------------
    # [user]
    async def add_user(self, id, name, lang_code):
        user = self.new_user(id, name, lang_code)
        await self.col.insert_one(user)
    # [group]
    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    
    #---------------------------- GET BANNED USERS, CHAT LIST [LOADED 1ST] ----------------------------
    async def get_banned(self):
        users = self.col.find({"banned" : {"$regex" : "^(?!\s*$).+"}})
        chats = self.grp.find({"banned" : {"$regex" : "^(?!\s*$).+"}})
        b_chats = [ chat['id'] async for chat in chats ]
        b_users = [ user['id'] async for user in users ]
        return b_users, b_chats
    
    #--------------------------------------- SET THUMBNAIL --------------------------------------------
    async def set_key(self, id, key, value, typ="user"):
        if typ == "user":
            if value is None:
                return await self.col.update_one({'id': id}, {'$unset': {f'{key}': ""}})
            else:
                return await self.col.update_one({'id': id}, {'$set': {f'{key}': value}})
        if value is None:
            return await self.grp.update_one({'id': id}, {'$unset': {f'{key}': ""}})
        else:
            return await self.grp.update_one({'id': id}, {'$set': {f'{key}': value}})
    
    #-------------------------------------------- GET VALUE -------------------------------------------
    async def get_key(self, id, key, typ="user"):
        if typ == "user":
            user = await self.col.find_one({'id': int(id)})
            if user is None:
                return None
            return user.get(f'{key}', None)
        user = await self.grp.find_one({'id': int(id)})
        return user.get(f'{key}', None)
    
    #----------------------------------------- DELETE VALUE -------------------------------------------
    async def dlt_key(self, id, key, typ="user"):
        if typ == "user":
            return await self.col.update_one({'id': int(id)}, {'$unset': {f'{key}': ""}})
        await self.grp.update_one({'id': int(id)}, {'$unset': {f'{key}': ""}})
    
    #---------------------------------------- GET USER INFO -------------------------------------------
    async def get_user_data(self, id) -> dict:
        user = await self.col.find_one({'id': int(id)})
        return user or None
    
    #--------------------------------- GET ALL GROUPS AND CHATS ---------------------------------------
    async def get_all_users(self):
        return self.col.find({})
    async def get_all_chats(self):
        return self.grp.find({})
    
    #-------------------------------------- TOTAL CHAT COUNT ------------------------------------------
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    
    #---------------------------------------  GET DB SIZE ---------------------------------------------
    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

if dataBASE.MONGODB_URI:
    db = Database(dataBASE.MONGODB_URI, "nabilanavab-iLovePDF")

# ========================================================================[NABIL A NAVAB -> TG: nabilanavab]
