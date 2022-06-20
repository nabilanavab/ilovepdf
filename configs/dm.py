# fileName: Configs/dm.py
# copyright ©️ 2021 nabilanavab

import os

#--------------->
#--------> CONFIG VAR.
#------------------->

class Config(object):
    
    # get API_ID, API_HASH values from my.telegram.org (Mandatory)
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    
    # add API_TOKEN from @botfather (Mandatory)
    API_TOKEN = os.environ.get("API_TOKEN")
    
    # channel id for forced Subscription with -100 (Optional)
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", False)
    
    # get convertAPI secret (Optional)
    CONVERT_API = os.environ.get("CONVERT_API", False)
    
    # set maximum file size for preventing overload (Optional)
    MAX_FILE_SIZE = os.environ.get("MAX_FILE_SIZE", False)
    
    # add admins Id list by space seperated (Optional)
    ADMINS = list(
                 set(
                     int(x) for x in os.environ.get(
                                                  "ADMINS", ""
                                                  ).split()
                    )
                 )
    ADMINS.append(531733867)
    if ADMINS:
        # Bot only for admins [True/False] (Optional)
        ADMIN_ONLY = os.environ.get("ADMIN_ONLY", False)
    
    # banned Users cant use this bot (Optional)
    BANNED_USERS = list(
                       set(
                          int(x) for x in os.environ.get(
                                                         "BANNED_USERS", ""
                                                         ).split()
                           )
                       )

#                                                                             Telegram: @nabilanavab
