import json
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
import boto3
from src.webhook_handler import handler
from src.record_table_manager import RecordTableManager
from liff.validation import validate_access_token
from liff.formatter import format_records


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


def data_handler(event, context):
    """
    For LIFF app
    if access_token is correct, return their studylog
    """
    validated = False
    records = None

    try:
        access_token = event["queryStringParameters"]["access_token"]
        user_id = event["queryStringParameters"]["user_id"]
        validated = validate_access_token(user_id, access_token)
    except:
        print("access_token or user_id was not passed correctly")

    if validated:
        dynamodb = boto3.resource('dynamodb')
        user_table = dynamodb.Table('record-studyhours-users')
        record_table = dynamodb.Table('record-studyhours-records')
        record_table_manager = RecordTableManager(user_table, record_table)

        all_user_records = record_table_manager.get_all_user_record(user_id)
        records = format_records(all_user_records)

    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {
                   "Access-Control-Allow-Origin": "*"
               },
               "body": json.dumps({
                   "message": "You are on the right track.",
                   "validated": validated,
                   "records": records
               })}

    print(event)

    return ok_json
