import logging
from urllib.parse import urljoin, urlencode, urlparse

import requests

from meme_police.bot_messages import get_random_duplicate_meme_message
from meme_police.downloaders import DOMAIN_IMAGE_DOWNLOADERS_MAP, download_image
from meme_police.env import TELGERAM_BOT_API_ENDPOINT
from meme_police.meme import upsert_picture_meme, meme_is_duplicate_by_image, meme_is_duplicate_by_url
from meme_police.utils.image import calculate_image_hash

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
    response = requests.get(url)
    logger.info(f'Got response status:\t{response.status_code}\t{response.content}')


def parse_meme_url(url):
    parsed_url = urlparse(url)

    # Remove subdomain
    domain = '.'.join(parsed_url.netloc.split('.')[-2:])

    return {
        'raw': url,
        'parsed': parsed_url,
        'domain': domain
    }


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

            parsed_url = parse_meme_url(url)

            if parsed_url['domain'] in DOMAIN_IMAGE_DOWNLOADERS_MAP:
                meme_urls.append(parsed_url)

        if entity['type'] == 'text_link':
            url = entity['url']
            parsed_url = parse_meme_url(url)

            if parsed_url['domain'] in DOMAIN_IMAGE_DOWNLOADERS_MAP:
                meme_urls.append(parsed_url)

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

    for meme_url_dict in parsed_message['meme_urls']:
        meme_url = meme_url_dict['raw']
        duplicate_reason = None
        image_hash = None

        if not duplicate_reason:
            if meme_is_duplicate_by_url(meme_url_dict, chat_id):
                duplicate_reason = 'url'

        if not duplicate_reason:
            image = download_image(meme_url_dict)
            image_hash = calculate_image_hash(image)

            if meme_is_duplicate_by_image(image_hash, chat_id):
                duplicate_reason = 'image'

        if not duplicate_reason:
            # Meme hasn't been posted before

            if not image_hash:
                image = download_image(meme_url_dict)
                image_hash = calculate_image_hash(image)

            upsert_picture_meme(meme_url_dict, image_hash, chat_id)
        else:
            send_message(
                get_random_duplicate_meme_message(meme_url, duplicate_reason),
                parsed_message['chat_id'],
                parsed_message['message_id']
            )

    if not parsed_message['meme_urls']:
        print("No meme urls :(")
