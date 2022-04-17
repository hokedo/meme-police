import json

import boto3

from meme_police.env import CHECK_MEME_QUEUE_URL


def push_to_check_meme_queue(message):
    """
    :param dict message:
    :return:
    """
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.Queue(CHECK_MEME_QUEUE_URL)

    json_message = json.dumps(message)

    queue.send_message(
        MessageBody=json_message,
        MessageAttributes={}
    )
