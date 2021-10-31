import json
import traceback

from meme_police.auth import is_authenticated
from meme_police.dynamodb import get_dynamo_db_pictures_table


def check_duplicate_meme(event, context):
    if not is_authenticated(event['headers']):
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Unauthorized'})
        }
    try:
        request_body = json.loads(event['body'])
        url_to_check = request_body['url']
        pictures_table = get_dynamo_db_pictures_table()
        entry = pictures_table().get_item(Key={'url': url_to_check})

        return json.dumps({
            'statusCode': 200,
            'body': json.dumps(entry)
        })
    except Exception as er:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(er),
                'traceback': traceback.format_exc()
            })
        }
