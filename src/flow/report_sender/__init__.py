from src.utils.timestamp import TimeStamp
from datetime import timedelta
from src.flow import Flow


class ReportSender(Flow):
    def __init__(self):
        self.timestamp = TimeStamp()
        self.datetimeFrom = None
        self.datetimeTo = None
        self.sum_data = {}
        self.avg_data = {}
        self.init_data()

    def divide_value(self, a, b):
        try:
            result = a / b
        except:
            return 0
        return result

    def init_data(self):
        self.sum_data = {
            "delivery_cnt": 0,
            "cancel_delivery_cnt": 0,
            "price": 0,
            "delivery_price": 0,
            "delivery_time": 0,
            "pickup_time": timedelta(0),
            "waiting_time": timedelta(0),
            "delivery_distance": 0,
        }

        self.avg_data = {
            "price": 0,
            "delivery_price": 0,
            "delivery_time": 0,
            "pickup_time": 0,
            "waiting_time": 0,
            "delivery_distance": 0,
        }

    def pre_process(self):
        pass

    def process(self):
        pass

    def run(self):
        pass

    def post_process(self):
        pass

    def get_date_range(self, parameter):
        today = self.timestamp.get_current_time_to_format("%y%m%d")
        datetimeFrom = None
        datetimeTo = None
        if parameter in ["daily", "day"]:
            datetimeFrom = self.timestamp.str_to_datetime(
                today + "000000", "%y%m%d%H%M%S"
            )
            datetimeTo = self.timestamp.str_to_datetime(
                today + "235959", "%y%m%d%H%M%S"
            )
        elif parameter in ["weekly", "week"]:
            datetimeFrom = (
                self.timestamp.first_day_in_week()
                .replace(hour=0)
                .replace(minute=0)
                .replace(second=0)
                .replace(microsecond=0)
            )
            datetimeTo = (
                self.timestamp.last_day_in_week()
                .replace(hour=23)
                .replace(minute=59)
                .replace(second=59)
                .replace(microsecond=999999)
            )
        elif parameter in ["monthly", "month"]:
            datetimeFrom = self.timestamp.first_day_in_month()
            datetimeTo = self.timestamp.last_day_in_month()

        return datetimeFrom, datetimeTo
