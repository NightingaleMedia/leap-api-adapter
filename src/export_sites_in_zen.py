from itertools import groupby
import json

from script.save_to_json import save_to_json


def filter_in_zen(site_list: list):
    sites_in_zen = filter(lambda item: item["InZen"] == "TRUE", site_list)
    return list(sites_in_zen)


if __name__ == "__main__":
    f = open("mock_leap_export.json")
    data = json.load(f)
    in_zen = filter_in_zen(data["data"])
    # filter by org
    key_func = lambda item: item["Zen Org ID"]
    region_func = lambda item: item["Zen Region ID"]
    in_zen = sorted(
        in_zen,
        key=key_func,
    )

    sorted_dict = []

    for key, value in groupby(in_zen, key_func):

        regions_list = []
        regions = sorted(list(value), key=region_func)

        for region_id, groups in groupby(regions, region_func):
            regions_list.append(dict({"region_id": region_id, "sites": list(groups)}))

        sorted_dict.append(dict({"org_id": key, "regions": list(regions_list)}))
    print(sorted_dict)
    # filter by region
    save_to_json(json_dict=dict({"orgs": sorted_dict}), filename="sites-in-zen")
