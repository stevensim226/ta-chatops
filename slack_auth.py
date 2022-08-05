import os
import time
import hashlib
import hmac

SIGNING_SECRET = os.environ.get("SIGNING_SECRET")
AUTHORIZED_WHITELIST_USERS = ["stevensim226"]
  
def is_authenticated_slack_request(timestamp, incoming_signature, data):
	if (int(time.time()) - int(timestamp)) > 60:
		print("Outdated (>60s) slack request detected!")
		return False

	slack_signing_secret = bytes(SIGNING_SECRET,"utf-8")

	basestring = f"v0:{timestamp}:{data}".encode("utf-8")
	result = "v0=" + hmac.new(slack_signing_secret, basestring, hashlib.sha256).hexdigest()

	return result == incoming_signature

def is_authorized_to_whitelist(username):
	return username in AUTHORIZED_WHITELIST_USERS