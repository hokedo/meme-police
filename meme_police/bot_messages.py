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


def get_random_duplicate_meme_message(meme_url, reason, parsed_message):
    user_id = parsed_message['from']['id']
    user_first_name = parsed_message['from']['first_name']
    user_last_name = parsed_message['from']['last_name']
    user_name = f"{user_first_name} {user_last_name}"
    user_mention_string = f"[{user_name}](tg://user?id={user_id})"

    insults = [
        "Te-am prins! Numa' zîc! Încercăm și noi mai mult?",
        f"Bă {user_mention_string} iară fuți meciu?",
        f"Voi mai puteți cu {user_mention_string} și meme-uri duplicate?",
        f"hahah mersi {user_mention_string}, sa nu consum curent degeaba",
        f"Mersi bosule, {user_mention_string}, incepeam să mă îngrijorez ca mă dă afară Bogdan",
        "Alex, tu l-ai pus să trimită?",
        "Eu am dat legi in țara asta! Tu dai duplicate, bă!"
    ]

    duplicate_reason_message = random.choice([
        f"Meme-ul a mai fost postat!\n{meme_url}"
    ])

    if reason == 'url':
        duplicate_reason_message = random.choice([
            f"URL-ul a mai fost postat!\n{meme_url}"
        ])

    if reason == 'image':
        duplicate_reason_message = random.choice([
            f"Poza a mai fost postata!\n{meme_url if meme_url else ''}"
        ])

    random_insult = random.choice(insults)

    return f'{duplicate_reason_message}\n\n{random_insult}'
