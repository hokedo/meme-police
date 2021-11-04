import imagehash

from .math import percentage


def calculate_image_hash(pil_image):
    return imagehash.phash(pil_image, 128)


def calculate_image_hash_similarity(hash_a, hash_b):
    hash_length = len(hash_a)
    return percentage(hash_a - hash_b, hash_length)
