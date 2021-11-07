import imagehash


def calculate_image_hash(pil_image):
    return imagehash.phash(pil_image, 128)


def calculate_image_hash_similarity(hash_a, hash_b):
    hash_length = len(hash_a)
    hash_difference = hash_a - hash_b

    return 1 - hash_difference / hash_length
