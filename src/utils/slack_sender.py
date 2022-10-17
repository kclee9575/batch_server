import requests
from src.utils.slack_webhook import SlackWebhook


class SlackSender:
    def __init__(self, category):
        # self.URL = "https://hooks.slack.com/services/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"  # #test-service-daily-report
        self.URL = self.get_url(category)
        self.slack = SlackWebhook(self.URL)

    def message_send(self, message):
        self.slack.send_format(message)

    def get_url(self, category):
        if category == "test-service-daily-report":
            return "https://hooks.slack.com/services/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"  # #test-service-daily-report
        elif category == "site_seven_eleven_poc":
            return "https://hooks.slack.com/services/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"
