import requests
import json
import os

POST_MSG_URL = "https://slack.com/api/chat.postMessage"
SLACK_TOKEN_HEADER = {
        "Authorization" : "Bearer " + os.environ.get("BOT_TOKEN"),
        "Content-Type": "application/json"
    }

def send_simple_message(channel, message):
    data = {"channel": channel, "text": message, "blocks": [build_text_block(message)]}
    requests.post(POST_MSG_URL, headers=SLACK_TOKEN_HEADER, data = json.dumps(data))

def build_text_block(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }