# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab


file_name = "ILovePDF/plugins/utils/work.py"

from plugins import *
from pyrogram import enums


async def work(
    message, work: str = "check", mtype: bool = True
) -> str:
    """
    program will now create a brand new directory to store all of your
    important user data depending up on chat_type

    Parameters:
    - message: The message or callback query from the user.
    - work: Action to perform: 'create', 'check', or 'delete'.
    - mtype: True if the message is a regular message, False if it's a callback query.

    Returns:
    - The path of the directory if created or checked, otherwise False.
    """
    if mtype:
        
        if message.chat.type == enums.ChatType.PRIVATE:
            # Create a path for private chats
            path = f"work/nabilanavab/{message.chat.id}"
        
        else:
            # Create a path for group chats including user ID
            pat = f"work/nabilanavab/{message.chat.id}"
            path = f"work/nabilanavab/{message.chat.id}/{message.from_user.id}"
    
    else:
        
        # If the message is a callback query
        if message.message is None:
            # inline query download cant get message from callback
            path = f"work/nabilanavab/inline{message.data.split('|')[2]}"
        
        elif message.message.chat.type == enums.ChatType.PRIVATE:
            # Create a path for private chats in callback queries
            path = f"work/nabilanavab/{message.message.chat.id}"
        
        else:
            # Create a path for group chats including user ID
            pat = f"work/nabilanavab/{message.message.chat.id}"
            path = f"work/nabilanavab/{message.message.chat.id}/{message.message.from_user.id}"
    
    if work == "create":
        
        # Check if the path already exists
        if os.path.exists(path):
            return False   # Return False if the path already exists
        
        os.makedirs(path)  # Create the directory
        return path        # Return the path of the created directory
    
    elif work == "check":
        # Check if the path exists
        return path if os.path.exists(path) else False
    
    elif work == "delete":
        
        # Handle directory deletion based on the context
        if (
            mtype
            and message.chat.type != enums.ChatType.PRIVATE
            and len(os.listdir(pat)) == 1
        ):
            return shutil.rmtree(pat, ignore_errors = True)
        
        elif not mtype and message.message is None:
            # inline message
            return shutil.rmtree(path, ignore_errors = True)
        
        elif (
            not mtype
            and message.message.chat.type != enums.ChatType.PRIVATE
            and len(os.listdir(pat)) == 1
        ):
            return shutil.rmtree(pat, ignore_errors = True)
        
        return shutil.rmtree(path, ignore_errors = True)


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD