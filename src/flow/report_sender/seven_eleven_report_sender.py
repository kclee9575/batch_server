from src.utils.database import seven_eleven_database
from src.utils.timestamp import TimeStamp
from . import ReportSender
from collections import defaultdict
from src.utils.slack_sender import SlackSender


class SevenElevenReportSender(ReportSender):
    def __init__(self, parameter):
        super().__init__()
        self.seven_eleven_database = seven_eleven_database
        self.sender = SlackSender("test-service-daily-report")
        self.timestamp = TimeStamp()
        self.parameter = parameter
        self.data_list = []
        self.divide_data_list = {}
        self.message_blocks = []

    def pre_process(self):
        super().pre_process()
        self.datetimeFrom, self.datetimeTo = self.get_date_range(self.parameter)
        self.data_list = self.get_data_list(
            f"SELECT * FROM orders where orderTime BETWEEN '{self.datetimeFrom}' AND '{self.datetimeTo}'"
        )
        self.divide_data_list = self.get_divide_data_list(self.data_list)

    def process(self):
        super().process()
        ## total data
        sum_data = self.get_sum_data(self.data_list)
        avg_data = self.get_avg_data(sum_data)
        self.message_header()
        self.message_content(sum_data, avg_data, "TOTAL")

        ## sep data
        for key in self.divide_data_list.keys():
            self.init_data()
            data_list = self.divide_data_list.get(key)
            sum_data = self.get_sum_data(data_list)
            avg_data = self.get_avg_data(sum_data)
            self.message_content(sum_data, avg_data, key)

    def post_process(self):
        super().post_process()
        message = {"blocks": self.message_blocks}
        self.sender.message_send(message)

    def run(self):
        super().run()
        try:
            self.pre_process()
        except Exception as e:
            print(f"pre_process error : {str(e)}")

        try:
            self.process()
        except Exception as e:
            print(f"process error : {str(e)}")

        try:
            self.post_process()
        except Exception as e:
            print(f"post_process error : {str(e)}")

    def get_divide_data_list(self, data_list):
        divide_data_list = defaultdict(list)
        for data in data_list:
            divide_data_list[data[4]].append(data)  # orderBranch ???????????? ??????
        return divide_data_list

    def get_data_list(self, sql):
        try:
            result = self.seven_eleven_database.fetch_all(sql)
        except Exception as e:
            result = []

        return result

    def get_sum_data(self, data_list):
        sum_data = self.sum_data
        for data in data_list:
            sum_data["delivery_cnt"] += 1
            sum_data["cancel_delivery_cnt"] += 0  # ?????? ??????
            sum_data["price"] += data[3]
            sum_data["delivery_price"] += 0  # ?????? ??????
            sum_data["delivery_time"] += data[7]
            sum_data["pickup_time"] += (
                data[12] - data[10]
            )  # ???????????????????????? ????????? ???????????? ?????? ????????? ????????????
            sum_data["waiting_time"] += (
                data[14] - data[13]
            )  # ??????????????????????????? ????????? ????????????(??????????????????)
            sum_data["delivery_distance"] += data[8]
        return sum_data

    def get_avg_data(self, data_list):
        avg_data = self.avg_data
        delivery_cnt = data_list.get("delivery_cnt")
        avg_data["price"] = (
            data_list.get("price") / delivery_cnt if delivery_cnt else 0
        )  # ?????? ??????
        avg_data["delivery_price"] = (
            data_list.get("delivery_price") / 1
        )  # ?????? ????????? # ?????? ??????
        avg_data["delivery_time"] = (
            data_list.get("delivery_time") / delivery_cnt if delivery_cnt else 0
        )  # ?????? ????????????
        avg_data["pickup_time"] = (
            data_list.get("pickup_time") / delivery_cnt if delivery_cnt else 0
        )  # ?????? ????????????
        avg_data["waiting_time"] = (
            data_list.get("waiting_time") / delivery_cnt if delivery_cnt else 0
        )  # ?????? ????????????
        avg_data["delivery_distance"] = (
            data_list.get("delivery_distance") / delivery_cnt if delivery_cnt else 0
        )  # ????????????
        return avg_data

    def message_header(self):
        self.message_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*[???????????????]* \n *{self.parameter.capitalize()} Report*  ( {self.datetimeFrom} ~ {self.datetimeTo} )",
                },
            }
        )

    def message_content(self, sum_data, avg_data, type):
        self.message_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*- {type}*",
                },
            }
        )
        self.message_blocks.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f">*??? ?????? ??????*\n>*?????? ?????? ??????*\n>*??? ?????? ??????*\n>*??? ?????????*\n>*?????? ?????? ??????*\n>*?????? ?????? ??????*\n>*?????? ?????? ??????*\n>*?????? ?????? ??????*",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"\n{sum_data.get('delivery_cnt')}???\n0???\n{sum_data.get('price')}???\n{sum_data.get('delivery_price')}???\n{avg_data.get('delivery_time')}???\n{avg_data.get('pickup_time')}\n{sum_data.get('waiting_time')}\n{avg_data.get('delivery_distance')}m",
                    },
                ],
            },
        )
