import json
import requests

import yaml

with open('domain.yml', 'r') as stream:
    try:
        domain = yaml.safe_load(stream)
        # print(domain)
    except yaml.YAMLError as exc:
        print(exc)

uid = '123'

tracker_rq = f"http://localhost:5005/conversations/{uid}/tracker"

# Check if user existed
tracker_result = json.loads(requests.get(tracker_rq).content)

if len(tracker_result["latest_message"]["intent"]) == 0:
    print("new_user")
    print(tracker_result['events'][1]['text']) # return init message conversation
else:
    print("old_user")

    user_message = "Ai day nhi"

    content = f'{{"text": "{user_message}", "sender": "user"}}'
    # print(content)

    reply_request = f"http://localhost:5005/conversations/{uid}/messages"

    reply_request_result = json.loads(requests.post(reply_request, data=content).content)
    # print(reply_request_result)

    next_action_request = f"http://localhost:5005/conversations/{uid}/predict"
    next_action_rq_result = json.loads(requests.post(next_action_request).content)

    next_action = next_action_rq_result["scores"][0]["action"]

    # intent = reply_request_result['latest_message']['intent']['name']

    result = domain['responses'][next_action][0]['text']

    print(result)