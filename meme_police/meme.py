import numpy as np
from boto3.dynamodb.conditions import Key, Attr
from imagehash import ImageHash

from meme_police.dynamodb import get_dynamo_db_pictures_table, get_dynamodb_client
from meme_police.utils.image import calculate_image_hash_similarity


def meme_is_duplicate(url_dict, chat_id):
    reason = None

    if meme_is_duplicate_by_url(url_dict, chat_id):
        reason = 'duplicate_url'

    elif meme_is_duplicate_by_image(url_dict, chat_id):
        reason = 'duplicate_image'

    return reason


def meme_is_duplicate_by_url(url_dict, chat_id):
    stripped_url = build_stripped_url(url_dict)

    pictures_table = get_dynamo_db_pictures_table()
    response = pictures_table.query(
        KeyConditionExpression=Key('stripped_url').eq(stripped_url),
        FilterExpression=Attr('chat_ids').contains(str(chat_id))
    )

    return response['Count'] > 0


def meme_is_duplicate_by_image(image_hash, chat_id):
    dynamo_db_client = get_dynamodb_client()
    pictures_table = get_dynamo_db_pictures_table()

    paginator = dynamo_db_client.get_paginator('scan')
    operation_parameters = {
        'TableName': pictures_table.table_name,
        'FilterExpression': 'contains(chat_ids, :chat_id)',
        'ExpressionAttributeValues': {
            ':chat_id': {'S': str(chat_id)},
        },
        'PaginationConfig': {
            'MaxItems': 100,
            'PageSize': 100,
        }
    }

    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        for item in page['Items']:
            other_image_hash = [item['BOOL'] for item in item['image_hash']['L']]
            other_image_hash = np.array(other_image_hash).reshape(image_hash.hash.shape)
            other_image_hash = ImageHash(other_image_hash)
            similarity = calculate_image_hash_similarity(image_hash, other_image_hash)

            if similarity >= 0.5:
                return True

    return False


def upsert_picture_meme(url_dict, image_hash, chat_id):
    stripped_url = build_stripped_url(url_dict)

    pictures_table = get_dynamo_db_pictures_table()
    return pictures_table.update_item(
        Key={'stripped_url': stripped_url},
        UpdateExpression='ADD chat_ids :new_chat_ids SET image_hash = :image_hash',
        ExpressionAttributeValues={
            ':new_chat_ids': {str(chat_id)},
            ':image_hash': [bool(item) for item in image_hash.hash.flatten()]
        },
        ReturnValues="UPDATED_NEW"
    )


def build_stripped_url(url_dict):
    domain = url_dict['domain']
    path = url_dict['parsed'].path
    return f'{domain}{path}'
