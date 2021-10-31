from functools import lru_cache

import boto3

from meme_police.env import DYNAMO_DB_PICTURES_TABLE_NAME


@lru_cache(maxsize=1)
def get_dynamodb_resource():
    return boto3.resource('dynamodb')


@lru_cache(maxsize=1)
def get_dynamo_db_pictures_table():
    return get_dynamodb_resource().Table(DYNAMO_DB_PICTURES_TABLE_NAME)
