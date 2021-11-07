import random


def get_random_busy_message():
    return random.choice([
        'Not right now',
        "Step aside, I've got other things to do",
        'No ticket today',
        '\**confused oinking*\*'
    ])


def get_random_greeting():
    return random.choice([
        'Hello there young memer'
    ])


def get_random_original_meme_message():
    return random.choice([
        'Looks like an original meme'
    ])


def get_random_duplicate_meme_message(meme_url, reason=None):
    if reason == 'url':
        return random.choice([
            f"Same URL was already posted!\n{meme_url}"
        ])

    if reason == 'image':
        return random.choice([
            f"Same Image was already posted!\n{meme_url if meme_url else ''}"
        ])

    return random.choice([
        f"Meme was already posted!\n{meme_url}"
    ])
