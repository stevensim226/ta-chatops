from slack_auth import is_authorized_to_whitelist
from slack_utils import send_simple_message, send_modal
from semaphore_utils import start_task_from_alias, WHITELIST_IP_TEMPLATE_NAME, SEMAPHORE_LOGS_URL, DEPLOY_APPSERVER_TEMPLATE_NAME
import json

WHITELIST_IP_MODAL_CALLBACK_ID = "whitelist_ip"
DEPLOYMENT_MODAL_CALLBACK_ID = "deploy_dev"

WHITELIST_IP_UNAUTHORIZED_MODAL = json.loads(open("modals/whitelist_unauthorized_modal.json").read())
WHITELIST_IP_MODAL = json.loads(open("modals/whitelist_modal.json").read())
DEPLOY_DEV_MODAL = json.loads(open("modals/deploydev_modal.json").read())

CHANNEL_NAME = "chatops-notifications"

CLOSE_MODAL_RESPONSE = {"response_action": "clear"}

def handle_shortcut(payload):
	shortcut_callback = payload["callback_id"]
	if shortcut_callback == WHITELIST_IP_MODAL_CALLBACK_ID:
		if is_authorized_to_whitelist(payload["user"]["username"]):
			to_be_sent_modal = WHITELIST_IP_MODAL
		else:
			to_be_sent_modal = WHITELIST_IP_UNAUTHORIZED_MODAL

		send_modal(payload["trigger_id"], to_be_sent_modal)
		return "OK"

	elif shortcut_callback == DEPLOYMENT_MODAL_CALLBACK_ID:
		send_modal(payload["trigger_id"], DEPLOY_DEV_MODAL)
		return "OK"


def handle_modal_submit(payload):
	callback_id = payload["view"]["callback_id"]
	requestor_username = payload["user"]["username"]
	
	if callback_id == WHITELIST_IP_MODAL_CALLBACK_ID:
		partner_name = payload["view"]["state"]["values"]["partner_name"]["partner_name"]["value"]
		partner_cidrs = payload["view"]["state"]["values"]["partner_cidrs"]["partner_cidrs"]["value"].strip()

		task_id = start_task_from_alias(WHITELIST_IP_TEMPLATE_NAME, env={
			"cidr_input": partner_cidrs,
			"partner_name": partner_name
		})

		send_simple_message(CHANNEL_NAME, f"IP whitelist request by @{requestor_username} for partner `{partner_name}` w/ IPs ```{partner_cidrs}``` (<{SEMAPHORE_LOGS_URL}{task_id}|Deployment Logs>)")

	elif callback_id == DEPLOYMENT_MODAL_CALLBACK_ID:
		branch_name = payload["view"]["state"]["values"]["branch_name"]["branch_name"]["value"]
		server_selection = payload["view"]["state"]["values"]["server_selection"]["server_selection"]["selected_option"]["value"]

		task_id = start_task_from_alias(DEPLOY_APPSERVER_TEMPLATE_NAME, env={
			"server_specifier": server_selection,
			"branch_name": branch_name,
			"requestor_username": requestor_username
		})

		send_simple_message(CHANNEL_NAME, f"Deployment for branch `{branch_name}` requested by @{requestor_username} to *{server_selection}* (<{SEMAPHORE_LOGS_URL}{task_id}|Deployment Logs>)")

	return CLOSE_MODAL_RESPONSE