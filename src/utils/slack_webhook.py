import requests


class SlackWebhook:
    def __init__(self, url):
        self.URL = url

    def send_format(self, message):
        payload = message
        requests.post(self.URL, json=payload)

    def send_text(self, message):
        payload = {"text": message}
        requests.post(self.URL, json=payload)
