import logging

import numpy as np
from boto3.dynamodb.conditions import Key, Attr
from imagehash import ImageHash

from meme_police.dynamodb import get_dynamo_db_pictures_table, get_dynamodb_client
from meme_police.env import IMAGE_SIMILARITY_THRESHOLD
from meme_police.utils.image import calculate_image_hash_similarity

logger = logging.getLogger(__name__)


def find_meme_by_url(url_dict, chat_id):
    stripped_url = build_stripped_url(url_dict)

    pictures_table = get_dynamo_db_pictures_table()
    response = pictures_table.query(
        KeyConditionExpression=Key('stripped_url').eq(stripped_url),
        FilterExpression=Attr('chat_id').eq(str(chat_id))
    )

    if response['Count'] > 0:
        logger.info("Similar meme found by url!")
        return response['Items'][0]

    logger.info("No similar meme found by url!")


def find_meme_by_image(image_hash, chat_id):
    logger.info(f"Looking for similar images in chat:\t{chat_id}")
    dynamo_db_client = get_dynamodb_client()
    pictures_table = get_dynamo_db_pictures_table()

    paginator = dynamo_db_client.get_paginator('scan')
    operation_parameters = {
        'TableName': pictures_table.table_name,
        'FilterExpression': 'chat_id = :current_chat_id',
        'ExpressionAttributeValues': {
            ':current_chat_id': {'S': str(chat_id)},
        },
        'PaginationConfig': {
            'MaxItems': 100,
            'PageSize': 100,
        }
    }

    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        for item in page['Items']:

            # If image has is empty, it has no image. Just URL was stored
            if item['image_hash']['L']:
                other_image_hash = [item['BOOL'] for item in item['image_hash']['L']]
                other_image_hash = np.array(other_image_hash).reshape(image_hash.hash.shape)
                other_image_hash = ImageHash(other_image_hash)
                similarity = calculate_image_hash_similarity(image_hash, other_image_hash)

                if similarity > IMAGE_SIMILARITY_THRESHOLD:
                    logger.info("Similar image found!")
                    item['chat_id'] = item['chat_id']['S']
                    item['original_message_id'] = item['original_message_id']['S']

                    return item

    logger.info("No similar image found!")


def insert_picture_meme(url_dict, image_hash, chat_id, original_message_id):
    stripped_url = build_stripped_url(url_dict)
    logger.info(f"Inserting picture meme:\t{stripped_url}")

    pictures_table = get_dynamo_db_pictures_table()
    return pictures_table.put_item(
        Item={
            'stripped_url': stripped_url,
            'chat_id': str(chat_id),
            'original_message_id': str(original_message_id),
            # If image hash not present, probably the meme is a video
            'image_hash': [
                bool(item)
                for item in image_hash.hash.flatten()
            ]
            if image_hash
            else []
        }
    )


def build_stripped_url(url_dict):
    domain = url_dict['domain']
    path = url_dict['parsed'].path
    return f'{domain}{path}'
