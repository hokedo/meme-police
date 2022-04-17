from meme_police.sqs import push_to_check_meme_queue

try:
    # requirements are zipped and slimmed when uploaded on lambda
    # this import will only work on the lambda instance
    import unzip_requirements
except ImportError:
    pass

import json
import logging
import traceback

from meme_police.telegram import handle_incoming_message, parse_telegram_webhook_body

logging.basicConfig(format="%(levelname)s\t%(asctime)s\t%(module)s\t%(message)s")

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def check_telegram_webhook_handler(event, context):
    response = {
        'statusCode': 200,
    }

    try:
        logger.info(f"Received event:\t{json.dumps(event)}")
        request_body = json.loads(event['body'])
        parsed_body = parse_telegram_webhook_body(request_body)

        if all([parsed_body['text'] or parsed_body['photo'], parsed_body['chat_id'], parsed_body['message_id']]):
            push_to_check_meme_queue(parsed_body)

    except Exception as er:
        response = {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(er),
                'traceback': traceback.format_exc()
            })
        }

    logger.info(f"Handler Response:\t{json.dumps(response)}")
    return response


def check_duplicate_meme_handler(event, context):
    logger.info(f"Received event:\t{json.dumps(event)}")
    from urllib.parse import ParseResult
    for record in event['Records']:
        item_body = json.loads(record['body'])
        for meme_url in item_body['meme_urls']:
            meme_url['parsed'] = ParseResult(*meme_url['parsed'])

        handle_incoming_message(item_body)
