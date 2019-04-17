import random

from linebot.models import (
    TextSendMessage,
    QuickReply,
    QuickReplyButton
    )

from linebot.models.actions import (
    DatetimePickerAction
)

from .time_manager import TimeManager

time_manager = TimeManager()


class MessageManager:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api

    def send_message(self, line_event, message, **kwargs):
        self.line_bot_api.reply_message(
            line_event.reply_token,
            TextSendMessage(text=message, **kwargs)
        )

    def send_follow_message(self, line_event):
        self.send_message(
            line_event,
            "友達登録ありがとう!\n"
            " -「勉強開始」で開始時間を記録\n"
            " -「勉強終了」で終了時間を記録\n"
            " -「勉強終了」し忘れたときは「終了忘れ」\n"
            "を送信してね!"
        )

    def send_start_confirmation(self, line_event):
        self.send_message(
            line_event,
            "勉強開始!!"
        )

    def send_end_confirmation(self, line_event):
        self.send_message(
            line_event,
            "勉強おわり!!"
        )

    def send_time_quickreply(self, line_event):
        self.send_message(
            line_event,
            "時間を選択してね!",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=DatetimePickerAction(
                        # to be modified
                        # if data is not specified, error occurs
                        label="時間設定",
                        mode="datetime",
                        initial=None,
                        max=None,
                        min=None,
                        data="quick_reply"
                    ))
                ]
            )
        )

    def send_settime_confirmation(self, line_event):
        self.send_message(
            line_event,
            "終了時間を設定したよ!"
        )

    def send_random_message(self, line_event):
        messages = ["ねみぃ"]
        self.send_message(
            line_event,
            random.choice(messages)
        )

    def send_bug_message(self, line_event):
        self.send_message(
            line_event,
            "バグかも?\n"
            "もしよければ開発者に現状のスクショを送ってあげて下さい!"
        )

    def send_studycheck_message(
            self,
            line_event,
            datetime_start,
            datetime_end):
        user_id = line_event.source.user_id
        user_profile = self.line_bot_api.get_profile(user_id)
        user_display_name = user_profile.display_name

        timedelta = datetime_end - datetime_start

        start_string = datetime_start.strftime("%m月%d日 %H時%M分")
        timedelta_string = time_manager.timedelta_to_string(timedelta)

        self.send_message(
            line_event,
            "{display_name}の最新の記録:\n"
            "{start}から{delta}の間勉強しました。\n"
            "詳細な記録を閲覧する機能は現在開発中です!".format(
                display_name=user_display_name,
                start=start_string,
                delta=timedelta_string
            )
        )
