import json
from msilib.schema import Error
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from script.call_google import call_google_maps
from script.location_service import format_for_zen, get_location
from script.config import SPREADSHEET_ID, SHEET
from script.write_to_sheet import write_to_sheet
from script.get_sheet_json import get_sheet_json
from script.save_to_json import save_to_json


RANGE_NAME = "NewMeterAssign!A:L"


def main():
    try:
        json_list: list = get_sheet_json(RANGE_NAME)
        error_list: list = []
        final_list: list = []
        # PARSE VALUES FROM RESULT
        final_list = call_google_maps(json_list=json_list)
        error_list = filter(lambda item: item["input_data"] is None, final_list)

        json_object = dict({"errors": list(error_list), "data": final_list})

        # Writing to sample.json
        save_to_json(json_dict=json_object, filename="leap_export")
        # Print columns A and E, which correspond to indices 0 and 4.
        write_to_sheet(final_list=final_list)
    except Error as err:
        print(err)


if __name__ == "__main__":
    main()
