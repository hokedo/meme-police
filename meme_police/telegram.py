import logging
from urllib.parse import urljoin, urlencode

import requests

from meme_police.bot_messages import get_random_busy_message, get_random_original_meme_message, get_random_greeting, \
    get_random_duplicate_meme_message
from meme_police.env import TELGERAM_BOT_API_ENDPOINT
from meme_police.meme import check_meme_by_url, upsert_picture_meme

logger = logging.getLogger(__name__)


def send_message(text, chat_id, message_id):
    message = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': message_id,
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
    message = body.get('message') or body.get('edited_message') or {}

    message_id = message.get('message_id')
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text')
    command, *arguments = text.split() if text else [None, None]

    return {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'command': command,
        'arguments': arguments,
    }


def handle_bot_command(parsed_message):
    command = parsed_message['command']
    arguments = parsed_message['arguments']
    chat_id = parsed_message['chat_id']

    if command == '/check_meme':
        meme_url = arguments[0]
        duplicate_reason = check_meme_by_url(meme_url, chat_id)
        if duplicate_reason:
            if duplicate_reason.get('url'):
                return get_random_duplicate_meme_message(reason='url')
            return get_random_duplicate_meme_message()

        # Meme hasn't been posted before
        upsert_picture_meme(meme_url, chat_id)
        return get_random_original_meme_message()

    if command == '/start':
        return get_random_greeting()

    return get_random_busy_message()
