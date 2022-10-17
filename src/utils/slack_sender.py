import requests
from src.utils.slack_webhook import SlackWebhook


class SlackSender:
    def __init__(self, category):
        self.URL = self.get_url(category)
        self.slack = SlackWebhook(self.URL)

    def message_send(self, message):
        self.slack.send_format(message)

    def get_url(self, category):

        if category == "test-service-daily-report":
            return "https://test_url"  # #test-service-daily-report
        elif category == "site_seven_eleven_poc":
            return "https://test_url"
