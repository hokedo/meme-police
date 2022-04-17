import os

IS_OFFLINE = os.environ.get('IS_OFFLINE', default=False)

DYNAMO_DB_PICTURES_TABLE_NAME = os.environ.get('PICTURES_TABLE_NAME', 'pictures')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', None)
TELGERAM_BOT_API_ENDPOINT = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
IMAGE_SIMILARITY_THRESHOLD = float(os.environ.get('IMAGE_SIMILARITY_THRESHOLD', 0.55))
CHECK_MEME_QUEUE_URL = os.environ.get('CHECK_MEME_QUEUE_URL')
