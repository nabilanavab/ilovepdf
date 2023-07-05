# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/logger.py"

import logging
logger = logging.getLogger(__name__)

# from configs.log import log
# LOG_FILE = log.LOG_FILE

logging.getLogger("PIL").setLevel(logging.ERROR)
logging.getLogger("fpdf").setLevel(logging.ERROR)
logging.getLogger("pikepdf").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("fontTools").setLevel(logging.ERROR)
logging.getLogger("PIL.Image").setLevel(logging.ERROR)
logging.getLogger("convertapi").setLevel(logging.ERROR)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

# SETING LOGGING INFO AS DEBUG
logging.basicConfig(
    # filemode = "a",
    level=logging.DEBUG,
    datefmt="%d-%b-%y %H:%M:%S",
    # filename = LOG_FILE if (LOG_FILE and LOG_FILE[-4:]==".log") else None,
    format="[%(asctime)s - %(name)s] : %(levelname)s - %(message)s",
)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
