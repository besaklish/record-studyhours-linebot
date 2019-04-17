import logging

logger = logging.getLogger(__name__)


class ActionManager:
    def __init__(
        self,
        user_table_manager,
        record_table_manager,
        time_manager,
        message_manager,
    ):
        self.user_table_manager = user_table_manager
        self.record_table_manager = record_table_manager
        self.time_manager = time_manager
        self.message_manager = message_manager

    def start_studying(self, line_event, user_id, timestamp):
        self.record_table_manager.put_new_record(user_id, timestamp)
        self.user_table_manager.set_user_latest_timestamp(user_id, timestamp)

        self.message_manager.send_start_confirmation(line_event)

        self.user_table_manager.set_user_status(user_id, "studying")

    def end_studying(self, line_event, user_id, timestamp):
        latest_record = self.record_table_manager.get_latest_record(user_id)
        self.record_table_manager.set_timestamp_end(latest_record, timestamp)

        self.message_manager.send_end_confirmation(line_event)

        self.user_table_manager.set_user_status(user_id, "freetime")

    def forget_studying(self, line_event, user_id):
        self.message_manager.send_time_quickreply(line_event)

        self.user_table_manager.set_user_status(user_id, "forgetting")

    def check_records(self, line_event, user_id):
        latest_record = self.record_table_manager.get_latest_record(user_id)
        datetime_start_utc = self.time_manager.line_timestamp_to_datetime(
            latest_record["timestamp_start"]
            )
        datetime_end_utc = self.time_manager.line_timestamp_to_datetime(
            latest_record["timestamp_end"]
            )

        datetime_start_jst = self.time_manager.utc_to_jst(datetime_start_utc)
        datetime_end_jst = self.time_manager.utc_to_jst(datetime_end_utc)

        self.message_manager.send_studycheck_message(
            line_event,
            datetime_start_jst,
            datetime_end_jst
        )

    def register_timestamp_end(self, line_event, user_id):
        try:
            endtime_string_from_line = line_event.postback.params["datetime"]
        except AttributeError:
            logger.warn(
                "Invalid message sent. It should be postback with datetime"
            )
            self.message_manager.send_time_quickreply(line_event)
            return

        try:
            endtime_jst = self.time_manager.line_datetime_string_to_datetime(
                endtime_string_from_line
                )
        except ValueError:
            logger.warn("ValueError: could not parse datetime object.")
            self.message_manager.send_bug_message(line_event)
            return

        endtime_utc = self.time_manager.jst_to_utc(endtime_jst)
        latest_record = self.record_table_manager.get_latest_record(user_id)
        # I want to check if timestamp_end is larger than timestamp_start
        # if not, I wanna send datetimepicker again
        timestamp_end = self.time_manager.datetime_to_line_timestamp(
            endtime_utc
            )
        self.record_table_manager.set_timestamp_end(
            latest_record,
            timestamp_end
            )

        self.message_manager.send_settime_confirmation(line_event)

        self.user_table_manager.set_user_status(user_id, "freetime")
