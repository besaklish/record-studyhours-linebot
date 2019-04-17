"""
There should be some way to check the entire study hours
maybe use LIFF?
"""
import logging
import datetime

import boto3

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage,
    FollowEvent, PostbackEvent
)

from .user_table_manager import UserTableManager
from .record_table_manager import RecordTableManager
from .message_manager import MessageManager
from .time_manager import TimeManager
from .action_manager import ActionManager

from .credentials import ACCESS_TOKEN, CHANNEL_SECRET

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('record-studyhours-users')
record_table = dynamodb.Table('record-studyhours-records')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

time_manager = TimeManager()
user_table_manager = UserTableManager(user_table, record_table)
record_table_manager = RecordTableManager(user_table, record_table)
message_manager = MessageManager(line_bot_api)

action_manager = ActionManager(
    user_table_manager,
    record_table_manager,
    time_manager,
    message_manager
)

logger = logging.getLogger(__name__)


@handler.add(FollowEvent)
def handle_follow(line_event):
    user_id = line_event.source.user_id
    display_name = line_bot_api.get_profile(user_id).display_name
    user_table_manager.put_user(user_id, display_name)
    user_table_manager.set_user_status(user_id, "freetime")

    logger.info("New user has been created.")

    message_manager.send_follow_message(line_event)


@handler.add(MessageEvent, message=TextMessage)
def handle_text(line_event):
    user_id = line_event.source.user_id
    user_status = user_table_manager.get_user_status(user_id)
    timestamp = line_event.timestamp

    if hasattr(line_event, "message"):
        message = line_event.message.text
    else:
        message = None

    start_messages = ["勉強開始", "開始", "start"]
    end_messages = ["勉強終了", "終了", "end", "finish", "done"]
    forget_messages = ["終了忘れ", "忘れ", "forget"]
    check_messages = ["勉強時間確認", "確認", "check"]

    if user_status == "freetime" and message in start_messages:
        action_manager.start_studying(line_event, user_id, timestamp)

    elif user_status == "studying" and message in end_messages:
        action_manager.end_studying(line_event, user_id, timestamp)

    elif user_status == "studying" and message in forget_messages:
        action_manager.forget_studying(line_event, user_id)

    elif user_status == "forgetting":
        message_manager.send_time_quickreply(line_event)

    elif message in check_messages:
        action_manager.check_records(line_event, user_id)

    else:
        message_manager.send_random_message(line_event)


@handler.add(PostbackEvent)
def handle_postback(line_event):
    user_id = line_event.source.user_id
    user_status = user_table_manager.get_user_status(user_id)

    if user_status == "forgetting":
        action_manager.register_timestamp_end(line_event, user_id)
