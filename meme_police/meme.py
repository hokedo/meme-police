from boto3.dynamodb.conditions import Key, Attr

from meme_police.dynamodb import get_dynamo_db_pictures_table


def meme_is_duplicate_by_url(url_to_check, chat_id):
    pictures_table = get_dynamo_db_pictures_table()
    response = pictures_table.query(
        KeyConditionExpression=Key('url').eq(url_to_check),
        FilterExpression=Attr('chat_ids').contains(str(chat_id))
    )

    return response['Count'] > 0


def upsert_picture_meme(url, chat_id):
    pictures_table = get_dynamo_db_pictures_table()
    return pictures_table.update_item(
        Key={'url': url},
        UpdateExpression='ADD chat_ids :new_chat_ids',
        ExpressionAttributeValues={
            ':new_chat_ids': {str(chat_id)}
        },
        ReturnValues="UPDATED_NEW"
    )
