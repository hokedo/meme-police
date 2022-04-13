import logging
from urllib.parse import urljoin, urlencode, urlparse

import requests

from meme_police.bot_messages import get_random_duplicate_meme_message
from meme_police.downloaders import DOMAIN_IMAGE_DOWNLOADERS_MAP, download_image, image_downloader_telegram
from meme_police.env import TELGERAM_BOT_API_ENDPOINT
from meme_police.meme import insert_picture_meme, find_meme_by_image, find_meme_by_url
from meme_police.utils.image import calculate_image_hash

logger = logging.getLogger(__name__)


def send_message(text, chat_id, reply_to_message_id):
    message = {
        'chat_id': chat_id,
        'text': text,
        'reply_to_message_id': reply_to_message_id,
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

    photo = message.get('photo', [])
    if photo:
        photo = sorted(photo, key=lambda x: x['file_size'], reverse=True)[0]

    message_from = message['from']

    return {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'command': command,
        'arguments': arguments,
        'entities': entities,
        'meme_urls': meme_urls,
        'photo': photo,
        'from': {
            'id': message_from['id'],
            'first_name': message_from.get('first_name') or '',
            'last_name': message_from.get('last_name') or '',
            'is_bot': message_from['is_bot'],
        },
    }


def handle_incoming_message(parsed_message):
    chat_id = parsed_message['chat_id']
    message_id = parsed_message['message_id']

    for meme_url_dict in parsed_message['meme_urls']:
        meme_url = meme_url_dict['raw']
        duplicate_reason = None
        image_hash = None

        original_meme = find_meme_by_url(meme_url_dict, chat_id)
        if original_meme:
            duplicate_reason = 'url'

        if not original_meme:
            image = download_image(meme_url_dict)

            if image:
                image_hash = calculate_image_hash(image)

                original_meme = find_meme_by_image(image_hash, chat_id)
                if original_meme:
                    duplicate_reason = 'image'
            else:
                logger.info(f"Failed to download image from '{meme_url}'")

        if not duplicate_reason:
            # Meme hasn't been posted before

            # if not image_hash:
            #     image = download_image(meme_url_dict)
            #     image_hash = calculate_image_hash(image)

            insert_picture_meme(meme_url_dict, image_hash, chat_id, message_id)
        else:
            send_reply_for_duplicate_meme(
                chat_id, duplicate_reason, meme_url, message_id, original_meme, parsed_message
            )

    if not parsed_message['meme_urls']:
        logger.info("No meme urls :(")

    if parsed_message['photo']:
        meme_url = ''
        file_id = parsed_message['photo']['file_id']

        image = image_downloader_telegram(file_id)
        if image:
            image_hash = calculate_image_hash(image)
            original_meme = find_meme_by_image(image_hash, chat_id)
            if original_meme:
                duplicate_reason = 'image'

                send_reply_for_duplicate_meme(
                    chat_id, duplicate_reason, meme_url, message_id, original_meme, parsed_message
                )
            else:
                meme_url_dict = {
                    'domain': 'telegram',
                    'parsed': urlparse(f"telegram/{file_id}")
                }
                insert_picture_meme(meme_url_dict, image_hash, chat_id, message_id)
        else:
            logger.info("Failed to download image from telegram")


def send_reply_for_duplicate_meme(chat_id, duplicate_reason, meme_url, message_id, original_meme, parsed_message):
    send_message(
        get_random_duplicate_meme_message(meme_url, duplicate_reason, parsed_message),
        chat_id,
        message_id
    )
    send_message(
        "Mesajul original",
        chat_id,
        original_meme['original_message_id']
    )
