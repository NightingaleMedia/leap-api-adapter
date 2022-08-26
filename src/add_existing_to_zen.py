from urllib.error import HTTPError
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
        url = f"{os.environ['ZEN_HQ_RELEASE']}/login"
        print(url)
        body = dict(
            {
                "email": f"{os.environ.get('ZEN_HQ_RELEASE_USERNAME')}",
                "password": f"{os.environ.get('ZEN_HQ_RELEASE_PASSWORD')}",
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


def add_group_to_zen(region_id, group_data):
    print(f'adding {group_data["title"]} to zen')
    url = f"{os.environ['ZEN_HQ_RELEASE']}/group"
    try:
        result = requests.post(url, headers=headers, json=group_data, verify=False)
        print(result.status_code)
        print(result.json())
    except HTTPError as e:
        group_data["error_details"] = dict(e)
        save_to_json(group_data, filename=f"exports/group-data--{group_data['title']}")
    print("waiting 5 sec")
    time.sleep(3)


def main():

    f = open("sites-in-zen.json")
    data = json.load(f)
    orgs = data["orgs"]

    for i, org in enumerate(orgs):
        print(f"adding {i} of {len(orgs)} to db")
        for i, region in enumerate(org["regions"]):
            # add to zen every site in this region
            for group in region["sites"]:
                group["input_data"]["parentId"] = region["region_id"]
                add_group_to_zen(
                    region_id=region["region_id"], group_data=group["input_data"]
                )


if __name__ == "__main__":
    main()
