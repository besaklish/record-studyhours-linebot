"""
方針
内部では基本的にUTCを扱う。つまり...
- UTCで送られてきた情報はそのまま扱う
- JSTで送られてきた情報は受け取った瞬間にUTCへ変換する
- ユーザーに時刻を表示する時はJSTへ変換する

今後追加でTimeDifferenceを設定できるようにしたい。LIFFを使用する。
"""
import datetime

JST = datetime.timezone(datetime.timedelta(hours=9))
UTC = datetime.timezone.utc


class TimeManager:
    def __init__(self):
        pass

    def utc_to_jst(self, utc_datetime):
        return utc_datetime.astimezone(JST)

    def jst_to_utc(self, jst_datetime):
        return jst_datetime.astimezone(UTC)

    def line_timestamp_to_datetime(self, line_timestamp):
        line_timestamp = float(line_timestamp)
        datetime_obj = datetime.datetime.fromtimestamp(line_timestamp / 1e3)
        return datetime_obj.replace(tzinfo=UTC)

    def line_datetime_string_to_datetime(self, line_datetime):
        datetime_obj = datetime.datetime.strptime(
            line_datetime,
            "%Y-%m-%dt%H:%M"
        )
        return datetime_obj.replace(tzinfo=JST)

    def datetime_to_line_timestamp(self, datetime_obj):
        return round(datetime_obj.timestamp() * 1000)

    def timedelta_to_string(self, timedelta):
        # add 1 min to prevent minus timedelta
        timedelta += datetime.timedelta(minutes=1)

        if timedelta.total_seconds() <= 0:
            timedelta = datetime.timedelta(seconds=0)

        totalseconds = round(timedelta.total_seconds())
        seconds = totalseconds % 60
        minutes = ((totalseconds - seconds) % (60 * 60)) / 60
        hours = (totalseconds - seconds - minutes * 60) / (60 * 60)

        minutes_int = int(minutes)
        hours_int = int(hours)

        return "{hours}時間{minutes}分".format(
            hours=hours_int,
            minutes=minutes_int
            )
