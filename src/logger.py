import logging
import os
import traceback

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'shop.log')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('BookShop')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console)


def log_error(message, exception=None):
    """Логирование ошибки со стеком вызовов"""
    if exception:
        logger.error(f"{message}: {exception}")
        logger.error(traceback.format_exc())
    else:
        logger.error(message)