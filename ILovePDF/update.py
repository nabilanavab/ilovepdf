# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2024 nabilanavab

# thank drxxstrange@gmail.com for update.py ♥️


file_name: str = "ILovePDF\update.py"

import os, logging, dotenv
from subprocess import run
from typing import List, Optional
from logging import FileHandler, StreamHandler, INFO, basicConfig

if os.path.exists("log.txt"):
    # Open in write mode to clear contents
    with open("log.txt", 'w') as f:
        pass

def setup_logging(
    format: str = "[%(asctime)s] [%(name)s | %(levelname)s] -" \
                  " %(message)s [%(filename)s:%(lineno)d]",
    datefmt: str = "%m/%d/%Y, %H:%M:%S %p",
    handlers: Optional[List[logging.FileHandler]] = None,
    level: int = INFO
) -> None:
    
    if handlers is None:
        handlers = [FileHandler('log.txt'), StreamHandler()]
    
    basicConfig(
        format = format,
        datefmt = datefmt,
        handlers = handlers,
        level = level
    )

    dotenv.load_dotenv('config.env', override = True)

setup_logging()

def update_repository(upstream_repo: str, upstream_branch: str) -> None:
    """
    Update the local Git repository from the specified upstream repository and branch.

    Args:
        upstream_repo (str): The URL of the upstream repository.
        upstream_branch (str): The branch to update from.
    """
    if upstream_repo:
        if os.path.exists('.git'):
            run(["rm", "-rf", ".git"])
        
        try:
            update = run(
                        f"git init -q &&"
                        f"git add . &&"
                        f"git commit -sm update -q &&"
                        f"git remote add origin {upstream_repo} &&"
                        f"git fetch origin -q &&"
                        f"git reset --hard origin/{upstream_branch} -q",
                        shell = True,
                        check = True
                    )
            if not update.returncode:
                log_info(f'Successfully updated with latest commit from {upstream_branch}')
        except Exception as e:
            log_error(f'Something went wrong while updating: %s', e)
            log_error(f'Check {upstream_repo} for validity and try again.')

update_repository(
    upstream_repo = os.getenv('upstream_repo'),
    upstream_branch = os.getenv('upstream_branch')
)


# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD