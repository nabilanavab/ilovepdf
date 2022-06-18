# fileName: configs/group.py
# copyright ©️ 2021 nabilanavab

import os

#--------------->
#--------> CONFIG VAR.
#------------------->

class groupConfig(object):
    
    # add admins Id list by space seperated (Optional)
    ADMIN_GROUPS = list(
                      set(
                         int(x) for x in os.environ.get(
                                                      "ADMIN_GROUPS", ""
                                                      ).split()
                         )
                      )
    
    # if admin group only (True)
    ADMIN_GROUP_ONLY = os.environ.get("ADMIN_GROUP_ONLY", False)
    
    # banned groups can't use this bot (Optional)
    BANNED_GROUP = list(
                       set(
                          int(x) for x in os.environ.get(
                                                      "BANNED_USERS", ""
                                                      ).split()
                          )
                       )
    
    ONLY_GROUP_ADMIN = os.environ.get("ONLY_GROUP_ADMIN", False)

#                                                                             Telegram: @nabilanavab
