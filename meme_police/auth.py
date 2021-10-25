import os
from base64 import b64encode


def is_authenticated(headers):
    username = os.environ.get("HARDCODED_USER", "")
    password = os.environ.get("HARDCODED_PASSWORD", "")
    expected_token = b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    return headers.get('Authorization') == f'Basic {expected_token}'
