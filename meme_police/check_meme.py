import json

from boto3.dynamodb.conditions import Key

from meme_police.dynamodb import get_dynamo_db_pictures_table
from meme_police.env import DYNAMO_DB_PICTURES_TABLE_NAME


def check_duplicate_meme(url_to_check):

    pictures_table = get_dynamo_db_pictures_table()
    response = pictures_table.query(
        KeyConditionExpression=Key('url').eq(url_to_check)
    )
    return response['Items']

