# fileName : plugins/logger.py
# copyright ©️ 2021 nabilanavab

import logging
logger = logging.getLogger(__name__)

#from configs.log import log
#LOG_FILE = log.LOG_FILE

logging.getLogger("PIL").setLevel(logging.ERROR)
logging.getLogger("pikepdf").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("PIL.Image").setLevel(logging.ERROR)
logging.getLogger("convertapi").setLevel(logging.ERROR)

# SETING LOGGING INFO AS DEBUG
logging.basicConfig(
                   # filemode = "a",
                   level = logging.DEBUG,
                   datefmt = '%d-%b-%y %H:%M:%S',
                   # filename = LOG_FILE if (LOG_FILE and LOG_FILE[-4:]==".log") else None,
                   format = "[%(asctime)s - %(name)s] : %(levelname)s - %(message)s",
                   )

# ======================================================================================================================================[NABIL A NAVAB -> TG: nabilanavab]
