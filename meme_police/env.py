import os

IS_OFFLINE = os.environ.get('IS_OFFLINE', default=False)

DYNAMO_DB_PICTURES_TABLE_NAME = os.environ['PICTURES_TABLE_NAME']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELGERAM_BOT_API_ENDPOINT = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
