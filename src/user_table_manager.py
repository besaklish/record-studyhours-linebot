import logging

logger = logging.getLogger(__name__)


class UserTableManager:
    def __init__(self, user_table, record_table):
        self.user_table = user_table
        self.record_table = record_table

    def put_user(self, user_id, display_name):
        self.user_table.put_item(
            Item={
                'id': user_id,
                'display_name': display_name
            }
        )

    def set_user_status(self, user_id, user_status):
        """
        user_status:
        - studying
        - freetime
        - forgetting
        """
        user_statuses = ["studying", "freetime", "forgetting"]
        if user_status not in user_statuses:
            logger.warn("You are trying to set invalid user_status to user.")
            return

        self.user_table.update_item(
            Key={
                'id': user_id
            },
            UpdateExpression="SET user_status = :s",
            ExpressionAttributeValues={
                ':s': user_status
            }
        )

    def get_user_status(self, user_id):
        response = self.user_table.get_item(
            Key={
                'id': user_id
            }
        )
        return response['Item']['user_status']

    def set_user_latest_timestamp(self, user_id, timestamp):
        self.user_table.update_item(
            Key={
                'id': user_id
            },
            UpdateExpression="SET latest_timestamp = :lts",
            ExpressionAttributeValues={
                ':lts': timestamp
            }
        )

    def get_user_latest_timestamp(self, user_id):
        response = self.user_table.get_item(
            Key={
                'id': user_id
            }
        )
        return response['Item']['latest_timestamp']
