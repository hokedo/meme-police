from urllib.parse import urlparse

from .downloaders import DOMAIN_IMAGE_DOWNLOADERS_MAP


def get_meme_urls_from_message(parsed_message):
    urls = []
    for entity in parsed_message['entities']:
        if entity['type'] == 'url':
            url_offset = entity['offset']
            url_length = entity['length']
            url = parsed_message['text'][url_offset:url_offset + url_length]
            parsed_url = urlparse(url)

            if parsed_url.netloc in DOMAIN_IMAGE_DOWNLOADERS_MAP:
                urls.append(url)

    return urls
