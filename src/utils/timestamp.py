from datetime import datetime, timedelta
from pytz import timezone
import calendar


class TimeStamp:
    def __init__(self, zone: str = "Asia/Seoul") -> None:
        self.zone: str = zone
        self.time = None

    def get_current_time(self):
        return datetime.now(timezone(self.zone))

    def get_current_utc_time(self):
        return datetime.now(timezone("UTC"))

    def get_current_time_to_format(self, format):
        return datetime.now(timezone(self.zone)).strftime(format)

    def first_day_in_week(self):  # 월요일
        return (self.get_current_time() - timedelta(days=1)) - timedelta(
            days=self.get_current_time().weekday()
        )

    def last_day_in_week(self):  # 일요일
        return (self.get_current_time() - timedelta(days=1)) + timedelta(
            days=(6 - self.get_current_time().weekday())
        )

    def first_day_in_month(self):
        return (self.get_current_time() - timedelta(days=1)).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

    def last_day_in_month(self):
        today = self.get_current_time() - timedelta(days=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        return today.replace(
            day=last_day, hour=23, minute=59, second=59, microsecond=999999
        )

    def str_to_datetime(self, str_date, format):
        return datetime.strptime(str_date, format)
