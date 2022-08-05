import requests
import json
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

POST_MSG_URL = "https://slack.com/api/chat.postMessage"
OPEN_MODAL_URL = "https://slack.com/api/views.open"

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

def send_modal(trigger_id, modal):
    requests.post(OPEN_MODAL_URL, json={
        "trigger_id": trigger_id,
        "view": modal
	}, headers={"Authorization": f"Bearer {BOT_TOKEN}"})