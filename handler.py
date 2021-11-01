import json
import logging
import traceback

from meme_police.telegram import handle_bot_command, parse_telegram_webhook_body, send_message

logging.basicConfig(
    format="%(levelname)s\t%(asctime)s\t%(module)s\t%(message)s",
    level=logging.INFO
)


def check_duplicate_meme_handler(event, context):
    try:
        request_body = json.loads(event['body'])
        parsed_body = parse_telegram_webhook_body(request_body)

        if all([parsed_body['text'], parsed_body['chat_id'], parsed_body['message_id']]):
            bot_response = handle_bot_command(parsed_body)
            send_message(bot_response, parsed_body['chat_id'], parsed_body['message_id'])

        return {
            'statusCode': 200,
            # 'body': json.dumps(result)
        }
    except Exception as er:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(er),
                'traceback': traceback.format_exc()
            })
        }
