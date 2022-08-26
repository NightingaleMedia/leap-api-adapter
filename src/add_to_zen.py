from script.save_to_json import save_to_json
import json


def get_token():
    return ""


def add_bulk_groups_to_zen(region_id, group_data):
    print(region_id)


def main():
    f = open("sites-in-zen.json")
    data = json.load(f)
    orgs = data["orgs"]

    for i, org in enumerate(orgs):
        bulk_add = dict()
        for region in org["regions"]:
            # add to zen every site in this region
            group_list = []
            for group in region["sites"]:
                group_list.append(group["input_data"])
            add_bulk_groups_to_zen(
                region_id=region["region_id"],
                group_data=group_list,
            )
            bulk_add[region["region_id"]] = group_list

        save_to_json(json_dict=bulk_add, filename=f"org-{i}")


if __name__ == "__main__":
    main()
