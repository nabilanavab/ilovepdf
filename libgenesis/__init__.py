import logging
from .search import Libgen

__version__ = '0.1.6'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger(__name__)
