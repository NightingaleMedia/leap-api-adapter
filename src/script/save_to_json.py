import json


def save_to_json(json_dict: dict, filename: str):
    json_object = json.dumps(json_dict, indent=4)
    with open(f"{filename}.json", "w") as outfile:
        outfile.write(json_object)
