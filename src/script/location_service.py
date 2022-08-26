import os
from script.response_shape import LocationResponse, LocationResults, LatLong
import requests
import time
import urllib.parse
from dotenv import load_dotenv

load_dotenv()


endpoint = "https://maps.googleapis.com/maps/api"
API_KEY = os.environ.get("GOOGLE_API_KEY")


def get_location(location_string: str):
    session = requests.Session()
    param_dict = {}
    param_dict["key"] = API_KEY
    query_string = urllib.parse.quote(location_string)
    param_dict["address"] = location_string
    request = requests.Request("GET", endpoint + "/geocode/json", params=param_dict)
    prepped = session.prepare_request(request)
    # print(format_prepped_request(prepped, 'utf8'))
    response = session.send(prepped)
    location_info = response.json()
    return location_info["results"][0]


def get_timezone(lat_lng: LatLong):
    param_dict = {}
    param_dict["key"] = API_KEY
    param_dict["location"] = f'{lat_lng["lat"]},{lat_lng["lng"]}'
    param_dict["timestamp"] = int(time.time())

    response = requests.get(endpoint + "/timezone/json", params=param_dict)
    return response.json()


def format_for_zen(org_title: str, loc_data, tz_data):
    response: dict = dict(
        {
            "title": org_title + " " + loc_data["formatted_address"],
            "location": {
                "address": loc_data["formatted_address"],
                "country": list(
                    filter(
                        lambda address_components: address_components[
                            "types"
                        ].__contains__("country"),
                        loc_data["address_components"],
                    )
                )[0][
                    "short_name"
                ],  # get country from address_components
                "state": list(
                    filter(
                        lambda address_components: address_components[
                            "types"
                        ].__contains__("administrative_area_level_1"),
                        loc_data["address_components"],
                    )
                )[0]["short_name"],
                # 'country': 'US',
                # 'state': 'CA', # get administrative_area_level_1 from address_components
                "timezone": tz_data["timeZoneId"],
                "utc_offset": tz_data["rawOffset"] + tz_data["dstOffset"],
                "lat": loc_data["geometry"]["location"]["lat"],
                "lng": loc_data["geometry"]["location"]["lng"],
            },
            "googlePlace": {
                "placeId": loc_data["place_id"],
                "url": "",
                "type": loc_data.get("types")[0] or "subpremise",
            },
        }
    )
    return response
