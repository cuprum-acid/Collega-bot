import os
from dotenv import load_dotenv

from logger import logger


load_dotenv()
logger.info(f'Loaded .env: {os.environ.values()}')


TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
STICKERS_NAME1 = os.environ.get('STICKERS_NAME1')
STICKERS_NAME2 = os.environ.get('STICKERS_NAME2')
SERVER_URL = os.environ.get('SERVER_URL')
REQUEST_INTERVAL = int(os.environ.get('REQUEST_INTERVAL'))
