"""
Validate LIFF Client
"""
import requests
import json


def validate_access_token(user_id, access_token):
    response = requests.get(
        "https://api.line.me/v2/profile",
        headers={
            "Authorization": "Bearer {}".format(access_token)},
        )

    print("response, raw text: " + response.text)

    response_dict = json.loads(response.text)

    print("response, userId: " + response_dict["userId"])
    print("userId from JS was: " + user_id)

    if response_dict["userId"] == user_id:
        return True

    return False
