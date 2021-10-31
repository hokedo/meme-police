import json
import traceback

from meme_police.auth import is_authenticated
from meme_police.check_meme import check_duplicate_meme


def check_duplicate_meme_handler(event, context):
    if not is_authenticated(event['headers']):
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Unauthorized'})
        }
    try:
        request_body = json.loads(event['body'])
        url_to_check = request_body['url']

        result = check_duplicate_meme(url_to_check)

        return json.dumps({
            'statusCode': 200,
            'body': json.dumps(result)
        })
    except Exception as er:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(er),
                'traceback': traceback.format_exc()
            })
        }
