from flask import Flask, request
from slack_auth import is_authenticated_slack_request
from slack_handlers import handle_shortcut, handle_modal_submit
import json

app = Flask(__name__)

SHORTCUT_OPEN_REQUEST = "shortcut"
SUBMIT_MODAL_REQUEST = "view_submission"

@app.route('/', methods=["POST"])
def chatops_entrypoint():
    if not is_authenticated_slack_request(
            request.headers["X-Slack-Request-Timestamp"],
            request.headers["X-Slack-Signature"],
            request.get_data().decode("ascii")):
        return "Request is invalid or expired", 403
    
    payload = json.loads(request.form["payload"])

    if payload["type"] == SHORTCUT_OPEN_REQUEST:
        return handle_shortcut(payload)
    
    elif payload["type"] == SUBMIT_MODAL_REQUEST:
        return handle_modal_submit(payload)

    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)