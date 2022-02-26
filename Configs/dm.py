# fileName: Configs/dm.py
# copyright ©️ 2021 nabilanavab




import os




#------------------------------------------- Config Variables -------------------------------------------

class Config(object):
    
    
    # get API_ID, API_HASH values from my.telegram.org (Mandatory)
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    
    
    # add API_TOKEN from @botfather (Mandatory)
    API_TOKEN = os.environ.get("API_TOKEN")
    
    
    # channel id for forced Subscription with -100 (Optional)
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL")
    
    
    # get convertAPI secret (Optional)
    CONVERT_API = os.environ.get("CONVERT_API")
    
    
    # set maximum file size for preventing overload (Optional)
    MAX_FILE_SIZE = os.environ.get("MAX_FILE_SIZE")
    
    
    # add admins Id list by space seperated (Optional)
    ADMINS = list(set(int(x) for x in os.environ.get("ADMINS", "0").split()))
    if ADMINS:
        # Bot only for admins [True/False] (Optional)
        ADMIN_ONLY = os.environ.get("ADMIN_ONLY", False)
    
    
    # banned Users cant use this bot (Optional)
    BANNED_USERS = list(set(int(x) for x in os.environ.get("BANNED_USERS", "0").split()))
    if not BANNED_USERS:
        BANNED_USERS = []
    
    # thumbnail
    PDF_THUMBNAIL = "./thumbnail.jpeg"
