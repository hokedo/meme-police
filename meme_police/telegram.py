import logging
from urllib.parse import urljoin, urlencode, urlparse

import requests

from meme_police.bot_messages import get_random_original_meme_message, get_random_duplicate_meme_message
from meme_police.downloaders import DOMAIN_IMAGE_DOWNLOADERS_MAP
from meme_police.env import TELGERAM_BOT_API_ENDPOINT
from meme_police.meme import meme_is_duplicate_by_url, upsert_picture_meme

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
    meme_urls = []

    for entity in entities:
        if entity['type'] == 'url':
            url_offset = entity['offset']
            url_length = entity['length']
            url = text[url_offset:url_offset + url_length]

            parsed_url = urlparse(url)
            domain = '.'.join(parsed_url.netloc.split('.')[-2:])

            if domain in DOMAIN_IMAGE_DOWNLOADERS_MAP:
                meme_urls.append(url)

    return {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'command': command,
        'arguments': arguments,
        'entities': entities,
        'meme_urls': meme_urls
    }


def handle_incoming_message(parsed_message):
    chat_id = parsed_message['chat_id']

    for meme_url in parsed_message['meme_urls']:
        duplicate_reason = meme_is_duplicate_by_url(meme_url, chat_id)

        if duplicate_reason:
            send_message(
                get_random_duplicate_meme_message(meme_url=meme_url, reason=duplicate_reason),
                parsed_message['chat_id'],
                parsed_message['message_id']
            )

        else:
            # Meme hasn't been posted before
            upsert_picture_meme(meme_url, chat_id)

    if not parsed_message['meme_urls']:
        print("No meme urls :(")
