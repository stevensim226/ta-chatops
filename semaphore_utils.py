import json
from re import template
import requests
import os

BASE_SEMAPHORE_API_URL = os.environ.get("BASE_SEMAPHORE_API_URL")
SEMAPHORE_LOGS_URL = f"{BASE_SEMAPHORE_API_URL}/project/1/history?t="
SEMAPHORE_HEADER = {"Authorization" : "Bearer " + os.environ.get("SEMAPHORE_TOKEN")}

WHITELIST_IP_TEMPLATE_NAME = "Whitelist Partner IP"
DEPLOY_APPSERVER_TEMPLATE_NAME = "Deploy Sample Appserver"

def get_template_id_by_alias(alias):
    url = f"{BASE_SEMAPHORE_API_URL}/api/project/1/templates"

    response = requests.get(url, headers=SEMAPHORE_HEADER)
    for template in response.json():
        if template["name"] == alias:
            return template["id"]

def start_task(template_id, debug=False, dry_run=False, playbook='', env={}):
    url = f"{BASE_SEMAPHORE_API_URL}/api/project/1/tasks"

    task_data = {
        "template_id": template_id,
        "debug": debug,
        "dry_run": dry_run,
        "playbook": playbook,
        "environment": json.dumps(env)
    }

    response = requests.post(url, headers=SEMAPHORE_HEADER, json=task_data)
    return response.json()["id"]

def start_task_from_alias(alias, **kwargs):
    template_id = get_template_id_by_alias(alias)
    return start_task(template_id, **kwargs)