from urllib.error import HTTPError
from script.add_created_group_to_sheet import add_created_group_to_sheet
from script.save_to_json import save_to_json
import json
import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()

TOKEN = ""


def get_token():
    global TOKEN
    if TOKEN == "":
        print("getting token")
        url = f"{os.environ['ZEN_HQ_PRODUCTION']}/login"
        print(url)
        body = dict(
            {
                "email": f"{os.environ.get('ZEN_HQ_PRODUCTION_USERNAME')}",
                "password": f"{os.environ.get('ZEN_HQ_PRODUCTION_PASSWORD')}",
            }
        )

        result = requests.post(url, json=body, verify=False)
        TOKEN = result.json()["data"]["token"]
        return result.json()["data"]["token"]
    else:
        print("already got token")
        return TOKEN


token = get_token()
headers = dict({"content-type": "application/json", "Authorization": f"Bearer {token}"})


def add_group_to_zen(group_data):
    print(f'adding {group_data["input_data"]["title"]} to zen')
    url = f"{os.environ['ZEN_HQ_PRODUCTION']}/group"
    body = {"data": group_data["input_data"]}
    try:
        # Add the group to zen prod
        result = requests.post(url, headers=headers, json=body, verify=False)
        print(result.status_code)
        # resulting group id will be in response
        created = result.json()
        # created = {"data": {"id": "TEST", "title": "TEST"}}

        # update a row in the spreadsheet to match group ID
        add_created_group_to_sheet(
            group_data,
            created_group_name=created["data"]["title"],
            created_group_id=created["data"]["id"],
            SPREADSHEET_ID="1NcBCbzBeQHMusSUQKkBEOqOYpBC_iwbZGeEhwYUf4tM",
            RANGE="ExportsFromScript!A:AA",
        )

    except HTTPError as e:
        group_data["error_details"] = dict(e)
        save_to_json(group_data, filename=f"exports/group-data--{group_data['title']}")
    print("waiting 1 sec")
    time.sleep(1)


def main():

    f = open("leap_export.json")
    data = json.load(f)

    for i, group in enumerate(data["data"]):
        # add to zen every site in this region
        print("in zen: " + group["InZen"])
        if group["InZen"] == "FALSE":
            print("adding...")
            group["input_data"]["parentId"] = group["Zen Region ID"]
            add_group_to_zen(group_data=group)


if __name__ == "__main__":
    main()
