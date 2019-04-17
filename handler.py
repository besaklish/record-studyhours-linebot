from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)

from src.webhook_handler import handler


def message_handler(event, context):
    signature = event["headers"]["X-Line-Signature"]
    body = event["body"]

    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {},
               "body": ""}
    error_json = {"isBase64Encoded": False,
                  "statusCode": 403,
                  "headers": {},
                  "body": "Error"}

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print(e)
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        return error_json
    except InvalidSignatureError:
        return error_json

    return ok_json
