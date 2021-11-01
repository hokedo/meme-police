from boto3.dynamodb.conditions import Key

from meme_police.dynamodb import get_dynamo_db_pictures_table


def check_meme_by_url(url_to_check):
    pictures_table = get_dynamo_db_pictures_table()
    response = pictures_table.query(
        KeyConditionExpression=Key('url').eq(url_to_check)
    )

    if response['Count'] > 0:
        return {'url': 1}


def insert_meme(url):
    pictures_table = get_dynamo_db_pictures_table()
    return pictures_table.put_item(Item={'url': url})
