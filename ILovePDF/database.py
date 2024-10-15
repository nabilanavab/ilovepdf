# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name: str = "ILovePDF/database.py"

# pip install motor
import datetime
from configs.db import dataBASE
from configs.config import settings
from typing import Dict, Any, Tuple, List
from motor.motor_asyncio import AsyncIOMotorClient, Cursor


class Database:
    """performs various operations on the database."""


    def __init__(self, uri: str, database_name: str) -> None:
        """
        Initialize the database connection.

        Args:
            uri (str): The URI for the MongoDB client.
            database_name (str): The name of the database to use.
        """
        # Creating a single instance
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        # clusters [users, group]
        self.col = self.db.users
        self.grp = self.db.groups


    def new_user(self, id: int, name: str, lang_code: str) -> Dict[str, Any]:
        """
        Add a new user to the database.

        Args:
            id (Any): The unique identifier for the user.
            name (str): The name of the user.
            lang_code (str): The language code of the user.

        Returns:
            Dict[str, Any]: A dictionary containing user information.
        """
        user_info = {
            "id" : id,
            "name" : name,
            "join_date" : datetime.date.today().isoformat()
        }
        if lang_code != settings.DEFAULT_LANG:
            user_info["lang"] = lang_code

        return user_info


    def new_group(self, id: int, title: str) -> dict:
        """
        Create a new group with the given ID and title.
        
        Args:
            id (int): The unique identifier for the group.
            title (str): The name of the group.

        Returns:
            dict: A dictionary containing the group's details, including
                the ID, title, and join date.
        """
        return dict(
            id = id,
            title = title,
            join_date = datetime.date.today().isoformat()
        )


    async def delete_user(self, user_id: int) -> dict:
        """
        Delete a user from the database.

        This method removes all records associated with the specified user ID
        from the users collection in the database.

        Args:
            user_id (int): The unique identifier of the user to be deleted.

        Returns:
            None: This method does not return a value.
        """
        await self.col.delete_many({"id": int(user_id)})

    
    async def is_user_exist(self, id: int) -> bool:
        """
        Check if a user exists in the database.

        Args:
            user_id (int): The unique identifier of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return bool(await self.col.find_one({"id": int(id)}))


    async def is_chat_exist(self, chat: int) -> bool:
        """
        Check if a chat (group) exists in the database.

        This method queries the groups collection to determine whether
        a chat with the specified ID exists. It returns True if the
        chat is found, and False otherwise.

        Args:
            chat_id (int): The unique identifier of the chat to check.

        Returns:
            bool: True if the chat exists, False otherwise.
        """
        return bool(await self.grp.find_one({"id": int(chat)}))


    async def add_user(self, id: int, name: str, lang_code: str) -> None:
        """
        Add a new user to the database.

        Args:
            user_id (int): The unique identifier for the user.
            name (str): The name of the user.
            lang_code (str): The language code associated with the user.

        Returns:
            None: This method does not return a value.
        """
        await self.col.insert_one(
            user = self.new_user(id, name, lang_code)
        )


    async def add_chat(self, chat: int, title: str) -> None:
        """
        Add a new chat (group) to the database.

        Args:
            chat_id (int): The unique identifier for the chat.
            title (str): The title of the chat.

        Returns:
            None: This method does not return a value.
        """
        await self.grp.insert_one(
            self.new_group(chat, title)
        )


    async def get_banned(self) -> Tuple[list[int], List[int]]:
        """
        Retrieve a list of banned users and chats from the database.

        This method queries the users and groups collections to find
        all entries where the 'banned' field is not empty or just whitespace.
        It returns two lists: one containing the IDs of banned users and
        the other containing the IDs of banned chats.

        Returns:
            Tuple[List[int], List[int]]: A tuple containing two lists:
                - A list of banned user IDs.
                - A list of banned chat IDs.
        """
        users = self.col.find({"banned": {"$regex": "^(?!\s*$).+"}})
        chats = self.grp.find({"banned": {"$regex": "^(?!\s*$).+"}})
        b_chats = [chat["id"] async for chat in chats]
        b_users = [user["id"] async for user in users]
        return b_users, b_chats


    async def get_beta(self) -> List[int]:
        """
        Retrieve a list of beta users from the database.

        Returns:
            List[int]: A list of beta user IDs.
        """
        users = self.col.find({"beta": {"$regex": "^(?!\s*$).+"}})
        beta_users = [user["id"] async for user in users]
        return beta_users


    async def set_key(self, id: int, key: str, value: Any, typ: str = "user") -> Dict:
        """
        Set a key-value pair for a user or group.
        
        If the value is None, the key will be removed
        from the database. The method operates differently depending on
        whether the 'typ' parameter is set to 'user' or 'group'
        
        Args:
            id (int): The unique identifier of the user or group.
            key (str): The key to be set or removed.
            value (Any): The value to be associated with the key. If None,
                        the key will be removed.
            typ (str): The type of entity to update ('user' or 'group').
                    Defaults to 'user'.

        Returns:
            Dict: Return rpdated user info.
        """
        if typ == "user":
            if value is None:
                return await self.col.update_one(
                    {"id": id}, {"$unset": {f"{key}": ""}}
                )
            else:
                return await self.col.update_one(
                    {"id": id}, {"$set": {f"{key}": value}}
                )
        if value is None:
            return await self.grp.update_one(
                {"id": id}, {"$unset": {f"{key}": ""}}
            )
        else:
            return await self.grp.update_one(
                {"id": id}, {"$set": {f"{key}": value}}
            )


    async def get_key(self, id: int, key: str, typ: str = "user") -> Any:
        """
        Retrieve the value of a specified key for a user or group.

        Args:
            id (int): The unique identifier of the user or group.
            key (str): The key whose value is to be retrieved.
            typ (str): The type of entity to check ('user' or 'group').
                    Defaults to 'user'.

        Returns:
            Any: The value associated with the key if found; None otherwise.
        """
        if typ == "user":
            user = await self.col.find_one({"id": int(id)})
            return user.get(f"{key}", None) or None
        group = await self.grp.find_one({"id": int(id)})
        return group.get(f"{key}", None) or None


    async def dlt_key(self, id: int, key: str, typ: str = "user") -> Any:
        """
        Delete specified key for a user or group.

        Args:
            id (int): The unique identifier of the user or group.
            key (str): The key whose value is to be retrieved.
            typ (str): The type of entity to check ('user' or 'group').
                    Defaults to 'user'.

        Returns:
            Any: The value associated with the key if found; None otherwise.
        """
        if typ == "user":
            return await self.col.update_one(
                {"id": int(id)}, {"$unset": {f"{key}": ""}}
            )
        return await self.grp.update_one(
            {"id": int(id)}, {"$unset": {f"{key}": ""}}
        )


    async def get_user_data(self, id: int) -> dict:
        """
        Retrieve user data from the database.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            dict: A dictionary containing the user's data if found;
                            None if the user does not exist.
        """
        return await self.col.find_one({"id": int(id)}) or None


    async def get_chat_data(self, id) -> dict:
        """
        Retrieve chat (group) data from the database.

        Args:
            chat_id (int): The unique identifier of the chat.

        Returns:
            dict: A dictionary containing the chat's data if found;
                            None if the chat does not exist.
        """
        return await self.grp.find_one({"id": int(id)}) or None


    async def get_all_users(self) -> Cursor:
        """
        Retrieve all users from the database.
        
        Returns:
            Cursor: An asynchronous cursor for the users collection.
        """
        return self.col.find({})


    async def get_all_chats(self) -> Cursor:
        """
        Retrieve all chats (groups) from the database.
        
        Returns:
            Cursor: An asynchronous cursor for the groups collection.
        """
        return self.grp.find({})
    

    async def total_users_count(self) -> int:
        """
        Get the total count of users in the database.

        Returns:
            int: The total number of users.
        """
        return await self.col.count_documents({})


    async def total_chat_count(self) -> int:
        """
        Get the total count of chats (groups) in the database.
        
        Returns:
            int: The total number of chats.
        """
        return await self.grp.count_documents({})


    async def get_db_size(self) -> int:
        """
        Retrieve the size of the database.

        Returns:
            int: The size of the database in bytes.
        """
        return (await self.db.command("dbstats"))["dataSize"]

if dataBASE.MONGODB_URI:
    db: Database = Database(dataBASE.MONGODB_URI, "nabilanavab-iLovePDF")


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
