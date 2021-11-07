from io import BytesIO
from urllib.parse import urljoin

import requests
from PIL import Image

CDN_IMAGES_URL_9GAG = 'https://img-9gag-fun.9cache.com/photo/'
CDN_IMAGES_URL_HUGELOL = 'https://hugelolcdn.com/i/'


def download_image(url_dict):
    domain = url_dict['domain']
    image_downloader = DOMAIN_IMAGE_DOWNLOADERS_MAP[domain]
    return image_downloader(url_dict)


def image_downloader_9gag(url_dict):
    post_id = url_dict['parsed'].path.split('/')[-1]
    image_url = urljoin(CDN_IMAGES_URL_9GAG, f'{post_id}_700b.jpg')
    response = requests.get(image_url)

    if response.ok:
        return Image.open(BytesIO(response.content))


def image_downloader_hugelol(url_dict):
    post_id = url_dict['parsed'].path.split('/')[-1]
    image_url = urljoin(CDN_IMAGES_URL_HUGELOL, f'{post_id}.jpg')
    response = requests.get(image_url)

    if response.ok:
        return Image.open(BytesIO(response.content))

    image_url = urljoin(CDN_IMAGES_URL_HUGELOL, f'{post_id}.png')
    response = requests.get(image_url)
    if response.ok:
        return Image.open(BytesIO(response.content))


DOMAIN_IMAGE_DOWNLOADERS_MAP = {
    '9gag.com': image_downloader_9gag,
    'hugelol.com': image_downloader_hugelol,
}
