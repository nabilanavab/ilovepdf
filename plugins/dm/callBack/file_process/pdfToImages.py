# fileName : plugins/dm/callBack/file_process/combinePages.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/combinePages.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

async def imageList(pages: str) -> ( bool, list ):
    """
    return a list with a specific range of numbers and some specific values from the input
    
    eg:
        '18:20,4,5,1:3'
        [1, 2, 3, 4, 5, 18, 19, 20]    <---return
    """
    try:
        for elem in input_str.split(','):
            if ':' in elem:
                start, end = map(int, elem.split(':'))
                my_list.extend(range(start, end+1, 1))
            else:
                my_list.append(int(elem))
        return True, sorted(set(my_list))
    except Exception as e:
        return False, Error

# Author: @nabilanavab
