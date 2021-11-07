#!/usr/bin/env python

import sys

from dotenv import load_dotenv
load_dotenv()

from meme_police.downloaders import download_image
from meme_police.telegram import parse_meme_url
from meme_police.utils.image import calculate_image_hash, calculate_image_hash_similarity



def compare_images(url_a, url_b):
    parsed_a = parse_meme_url(url_a)
    parsed_b = parse_meme_url(url_b)

    img_a = download_image(parsed_a)
    img_b = download_image(parsed_b)

    hash_a = calculate_image_hash(img_a)
    hash_b = calculate_image_hash(img_b)

    similarity = calculate_image_hash_similarity(hash_a, hash_b)

    print(similarity)


compare_images(sys.argv[1], sys.argv[2])
