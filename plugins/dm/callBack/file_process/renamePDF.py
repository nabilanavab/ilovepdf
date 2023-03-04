# fileName : plugins/dm/callBack/file_process/blackAndWhitePdf.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/blackAndWhitePdf.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

async def renamePDF(input_file: str):
    """
    Renaming PDF files can help you keep your files organized and easy to find.
    By giving the file a descriptive name that reflects its contents, you can
    quickly identify the file you need without having to open it.
    
    parameter:
        input_file : Here is the path of the file that the user entered
        
    return:
        bool        : Return True when the request is successful
        input_file : This is the path where the output file can be found.
    """
    return True, input_file


# Author: @nabilanavab
