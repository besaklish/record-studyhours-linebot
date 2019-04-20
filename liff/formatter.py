from src.time_manager import TimeManager

time_manager = TimeManager()


def _format_record(record):
    user_id = record["user_id"]
    timestamp_start = float(record["timestamp_start"])
    timestamp_end = float(record["timestamp_end"])

    datetime_start = time_manager.line_timestamp_to_datetime(timestamp_start)
    datetime_end = time_manager.line_timestamp_to_datetime(timestamp_end)

    timedelta_string = time_manager.timedelta_to_string(
      datetime_end - datetime_start
      )
    datetime_start_jst = time_manager.utc_to_jst(datetime_start)
    time_start_string = datetime_start_jst.isoformat()

    return dict(
            user_id=user_id,
            start=time_start_string,
            timedelta=timedelta_string,
        )


def format_records(records):
    return [_format_record(record) for record in records]
