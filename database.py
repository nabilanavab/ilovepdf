# fileName : database.py
# copyright ©️ 2021 nabilanavab

# pip install motor

import datetime
import motor.motor_asyncio
from configs.db import dataBASE
from configs.db import isMONGOexist

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
    def new_user(self, id, name):
        return dict(
                   id = id,
                   name = name,
                   join_date = datetime.date.today().isoformat(),
                   thumbnail = None,
                   convertAPI = None,
                   ban_status = dict(
                           is_banned = False,
                           ban_reason = ""
                   ))
    
    #ADD NEW GROUP TO DB
    def new_group(self, id, title):
        return dict(
                   id = id,
                   title = title,
                   join_date = datetime.date.today().isoformat(),
                   thumbnail = None,
                   convertAPI = None,
                   chat_status = dict(
                            is_disabled = False,
                            ban_reason = ""
                   ))
    
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
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    # [group]
    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    
    #----------------------------------- DELETE USER FROM DB -----------------------------------------
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    
    #------------------------------------------- BAN -------------------------------------------------
    # [user]
    async def ban_user(self, user_id, ban_reason = "No Reason"):
        ban_status = dict(
                       is_banned = True,
                       ban_reason = ban_reason
                       )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})
    # [group]
    async def disable_chat(self, chat, reason="No Reason"):
        chat_status = dict(
                          is_disabled = True,
                          reason = reason
                          )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
    
    #------------------------------------------- UNBAN -----------------------------------------------
    # [user]
    async def remove_ban(self, id):
        ban_status = dict(
                         is_banned = False,
                         ban_reason = ''
                         )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    # [group]
    async def re_enable_chat(self, id):
        chat_status = dict(
                          is_disabled = False,
                          reason = ""
                          )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
    
    #-------------------------------------- GET BAN STATUS -------------------------------------------
    # [user]
    async def get_ban_status(self, id):
        default = dict(
                     is_banned = False,
                     ban_reason = ''
                     )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)
    # [group]
    async def get_grup_status(self, id):
        default = dict(
                      is_banned = False,
                      ban_reason = ''
                      )
        user = await self.grp.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)
    
    #---------------------------- GET BANNED USERS, CHAT LIST [LOADED 1ST] ----------------------------
    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats
    
    #--------------------------------------- SET THUMBNAIL --------------------------------------------
    # [user]
    async def set_thumbnail(self, id, thumbnail):
        await self.col.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})
    # [group]
    async def set_group_thumb(self, id, thumbnail):
        await self.grp.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})
    
    #--------------------------------------- GET THUMBNAIL -------------------------------------------
    # [user]
    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail', None)
    # [group]
    async def get_group_thumb(self, id):
        user = await self.grp.find_one({'id': int(id)})
        return user.get('thumbnail', None)
    
    #----------------------------- SET CONVERTAPI FOR PDF FILES ---------------------------------------
    async def set_convertAPI(self, id, convertAPI):
        await self.col.update_one({'id': id}, {'$set': {'convertAPI': convertAPI}})
    # GET CONVERTAPI
    async def get_convertAPI(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('convertAPI', None)
    
    #-------------------------------------- GET USER INFO ---------------------------------------------
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

if isMONGOexist:
    db = Database(
                 dataBASE.MONGODB_URI,
                 "nabilanavab-iLovePDF"
                 )

#                                                                             Telegram: @nabilanavab
