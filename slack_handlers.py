from slack_auth import is_authorized_to_whitelist
import requests
import os
import json

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPEN_MODAL_URL = "https://slack.com/api/views.open"

WHITELIST_IP_MODAL_CALLBACK_ID = "whitelist_ip"

WHITELIST_IP_UNAUTHORIZED_MODAL = json.loads(open("modals/whitelist_unauthorized_modal.json").read())
WHITELIST_IP_MODAL = json.loads(open("modals/whitelist_modal.json").read())

CLOSE_MODAL_RESPONSE = {"response_action": "clear"}

def handle_shortcut(payload):
	if payload["callback_id"] == WHITELIST_IP_MODAL_CALLBACK_ID:
		if is_authorized_to_whitelist(payload["user"]["username"]):
			to_be_sent_modal = WHITELIST_IP_MODAL
		else:
			to_be_sent_modal = WHITELIST_IP_UNAUTHORIZED_MODAL

		requests.post(OPEN_MODAL_URL, json={
			"trigger_id": payload["trigger_id"],
			"view": to_be_sent_modal
		}, headers={"Authorization": f"Bearer {BOT_TOKEN}"})

		return "OK"

def handle_modal_submit(payload):
	if payload["view"]["callback_id"] == WHITELIST_IP_MODAL_CALLBACK_ID:
		partner_name = payload["view"]["state"]["values"]["partner_name"]["partner_name"]["value"]
		partner_cidrs = payload["view"]["state"]["values"]["partner_cidrs"]["partner_cidrs"]["value"].split()
		print(partner_name, partner_cidrs)

	return CLOSE_MODAL_RESPONSE