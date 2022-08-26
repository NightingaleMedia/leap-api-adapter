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
    print(f'adding {group_data["input_data"]["title"]} to zen')
    url = f"{os.environ['ZEN_HQ_RELEASE']}/group"
    body = {"data": group_data["input_data"]}
    try:
        result = requests.post(url, headers=headers, json=body, verify=False)
        print(result.status_code)
        created = result.json()
        # created = {"data": {"id": "TEST", "title": "TEST"}}
        add_created_group_to_sheet(
            group_data,
            created_group_name=created["data"]["title"],
            created_group_id=created["data"]["id"],
            SPREADSHEET_ID="1fuFt4_R-wH7hoCICOE8MlrpcOeEKlGMKNFS0VVvf_5c",
            RANGE="ExportsFromScript!A:AA",
        )

    except HTTPError as e:
        group_data["error_details"] = dict(e)
        save_to_json(group_data, filename=f"exports/group-data--{group_data['title']}")
    print("waiting 3 sec")
    time.sleep(3)


def main():

    f = open("mock_leap_export.json")
    data = json.load(f)
    orgs = data["orgs"]

    for i, org in enumerate(orgs):
        print(f"adding {i} of {len(orgs)} to db")
        for i, region in enumerate(org["regions"]):
            # add to zen every site in this region
            for group in region["sites"]:
                if group["InZen"] == "FALSE" and group["input_data"] is not None:
                    group["input_data"]["parentId"] = region["region_id"]
                    add_group_to_zen(region_id=region["region_id"], group_data=group)


if __name__ == "__main__":
    main()
