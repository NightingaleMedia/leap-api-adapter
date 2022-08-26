from concurrent.futures.thread import ThreadPoolExecutor
from script.location_service import format_for_zen, get_timezone, get_location


def get_location_data(item):
    try:
        loc_data = get_location(item["ServiceAddress"])
        tz_data = get_timezone(loc_data["geometry"]["location"])
        item["input_data"] = format_for_zen(
            item["Zen Org Name"], loc_data=loc_data, tz_data=tz_data
        )
    except Exception:
        print("error")
        item["input_data"] = None
    return item


def call_google_maps(json_list: list):
    final_list: list = []
    completed = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        completed = executor.map(get_location_data, json_list)

    final_list.extend(completed)
    return final_list
    # for index, item  in enumerate(json_list):
    #     try:
    #         item["input_data"] = format_for_zen(item['ServiceAddress'], item['Zen Org Name'])
    #     except:
    #         error_item = json_list.pop(index)
    #         error_list.append(error_item)
