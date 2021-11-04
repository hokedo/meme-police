from io import BytesIO
from urllib.parse import urlparse, urljoin

import requests
from PIL import Image

CDN_IMAGES_URL_9GAG = 'https://img-9gag-fun.9cache.com/photo/'
CDN_IMAGES_URL_HUGELOL = 'https://hugelolcdn.com/i/'


def image_downloader_9gag(url):
    post_id = urlparse(url).path.split('/')[-1]
    image_url = urljoin(CDN_IMAGES_URL_9GAG, f'{post_id}_700b.jpg')
    response = requests.get(image_url)

    if response.ok:
        return Image.open(BytesIO(response.content))


def image_downloader_hugelol(url):
    post_id = urlparse(url).path.split('/')[-1]
    image_url = urljoin(CDN_IMAGES_URL_HUGELOL, f'{post_id}.jpg')
    response = requests.get(image_url)

    if response.ok:
        return Image.open(BytesIO(response.content))


DOMAIN_IMAGE_DOWNLOADERS_MAP = {
    '9gag.com': image_downloader_9gag,
    'hugelol.com': image_downloader_hugelol,
}
