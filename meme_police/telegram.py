import logging
from urllib.parse import urljoin, urlencode

import requests

from meme_police.bot_messages import get_random_original_meme_message, get_random_duplicate_meme_message
from meme_police.env import TELGERAM_BOT_API_ENDPOINT
from meme_police.meme import meme_is_duplicate_by_url, upsert_picture_meme
from meme_police.utils import get_meme_urls_from_message

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
    entities = message.get('entities', [])

    return {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'command': command,
        'arguments': arguments,
        'entities': entities,
    }


def handle_incoming_message(parsed_message):
    chat_id = parsed_message['chat_id']

    meme_urls = get_meme_urls_from_message(parsed_message)
    for meme_url in meme_urls:
        is_duplicate = False

        if meme_is_duplicate_by_url(meme_url, chat_id):
            is_duplicate = True
            send_message(
                get_random_duplicate_meme_message(meme_url=meme_url, reason='url'),
                parsed_message['chat_id'],
                parsed_message['message_id']
            )

        if not is_duplicate:
            # Meme hasn't been posted before
            upsert_picture_meme(meme_url, chat_id)
            return get_random_original_meme_message()

    # if command == '/start':
    #     return get_random_greeting()
    #
    # return get_random_busy_message()
