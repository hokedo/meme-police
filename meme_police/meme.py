from boto3.dynamodb.conditions import Key, Attr

from meme_police.dynamodb import get_dynamo_db_pictures_table


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


def meme_is_duplicate_by_image(url_to_check, chat_id):
    pass


def upsert_picture_meme(url_dict, chat_id):
    stripped_url = build_stripped_url(url_dict)

    pictures_table = get_dynamo_db_pictures_table()
    return pictures_table.update_item(
        Key={'stripped_url': stripped_url},
        UpdateExpression='ADD chat_ids :new_chat_ids',
        ExpressionAttributeValues={
            ':new_chat_ids': {str(chat_id)}
        },
        ReturnValues="UPDATED_NEW"
    )


def build_stripped_url(url_dict):
    domain = url_dict['domain']
    path = url_dict['parsed'].path
    return f'{domain}{path}'
