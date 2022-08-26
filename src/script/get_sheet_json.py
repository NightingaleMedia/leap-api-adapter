import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from script.call_google import call_google_maps
from script.location_service import format_for_zen, get_location
from script.config import SPREADSHEET_ID, SHEET
from script.write_to_sheet import write_to_sheet


def get_sheet_json(range_name: str):
    try:
        result = (
            SHEET.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        )
        values: list = result.get("values", [])

        if not values:
            print("No data found.")
            return
        titles = values.pop(0)
        json_list: list = []

        # PARSE VALUES FROM RESULT
        for row in values:
            item = dict()
            for index, value in enumerate(titles):
                try:
                    row[index]
                except IndexError:
                    row.append(None)
                finally:
                    item[value] = row[index]
            json_list.append(item)
        return json_list
    except HttpError as err:
        print(err)
