import logging
import random
from urllib.parse import urljoin, urlencode

import requests

from meme_police.check_meme import check_duplicate_meme
from meme_police.env import TELGERAM_BOT_API_ENDPOINT

logger = logging.getLogger(__name__)


def send_message(text, chat_id):
    message = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    urlencoded_message = urlencode(message)

    url = urljoin(TELGERAM_BOT_API_ENDPOINT, f'sendMessage?{urlencoded_message}')
    logger.info(f'Requesting url:\t{url}')
    print(f'Requesting url:\t{url}')
    response = requests.get(url)

    logger.info(f'Got response status:\t{response.status_code}\t{response.content}')
    print(f'Got response status:\t{response.status_code}\t{response.content}')


def parse_telegram_webhook_body(body):
    message = body.get('message') or body.get('edited_message')

    chat_id = message['chat']['id']
    command_arguments = message['text'].split()
    command, *arguments = command_arguments

    return {
        'chat_id': chat_id,
        'command': command,
        'arguments': arguments
    }


def handle_bot_command(command, arguments):
    if command == '/check_meme':
        duplicate_meme = check_duplicate_meme(arguments[0])
        if duplicate_meme:
            return f"Meme was already posted!\n{arguments[0]}"
        return "Looks like an original meme"

    if command == '/start':
        return "Hello there young memer"

    return random.choice([
        "Not right now",
        "Step aside, I've got other things to do",
        "No ticket today",
        "\**confused oinking*\*"
    ])
