import logging
from datetime import datetime

from boto3.dynamodb.conditions import Attr

from .user_table_manager import UserTableManager

logger = logging.getLogger(__name__)


class RecordTableManager:
    def __init__(self, user_table, record_table):
        self.user_table = user_table
        self.record_table = record_table

    def put_new_record(self, user_id, timestamp_start):
        self.record_table.put_item(
            Item={
                'user_id': user_id,
                'timestamp_start': timestamp_start
            }
        )

        logger.info(
            "Successfully created a record: "
            "user_id: {}, timestamp_start: {}".format(
                user_id,
                timestamp_start
            )
        )

    def get_latest_record(self, user_id):
        user_table_manager = UserTableManager(
            self.user_table, self.record_table
            )
        latest_timestamp = user_table_manager.get_user_latest_timestamp(
            user_id
            )

        latest_record = self.record_table.get_item(
            Key={
                "user_id": user_id,
                "timestamp_start": latest_timestamp
            }
        )["Item"]

        print("latest_record: " + str(latest_record))
        return latest_record

    def set_timestamp_end(self, latest_record, timestamp_end):
        user_id = latest_record["user_id"]
        timestamp_start = latest_record["timestamp_start"]

        self.record_table.update_item(
            Key={
                "user_id": user_id,
                "timestamp_start": timestamp_start
            },
            UpdateExpression="set timestamp_end = :te",
            ExpressionAttributeValues={
                ":te": timestamp_end
            }
        )
