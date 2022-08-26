import json
from pprint import pprint
from googleapiclient.errors import HttpError
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from script.config import SHEET, SPREADSHEET_ID

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# # The ID and range of a sample spreadsheet.
# SPREADSHEET_ID = "1NcBCbzBeQHMusSUQKkBEOqOYpBC_iwbZGeEhwYUf4tM"


# creds = service_account.Credentials.from_service_account_file(
#     "credentials.json", scopes=SCOPES
# )
# service = build("sheets", "v4", credentials=creds)
# # Call the Sheets API
# sheet = service.spreadsheets()


RANGE_NAME = "PythonExport!A:AA"


def write_to_sheet(final_list: list):
    write_headers = [
        "Zen Org Id",
        "Zen Org Name",
        "Old Address",
        "Formatted Address",
        "In Zen",
        "Zen Group ID",
    ]

    write_values = []
    for location in final_list:
        formatted_address = (
            location["input_data"]
            and location["input_data"]["location"]["address"]
            or None
        )
        write_values.append(
            [
                location["Zen Org ID"],
                location["Zen Org Name"],
                location["ServiceAddress"],
                formatted_address,
                location["InZen"] == "TRUE",
                location["Zen Region ID"] or "",
                location["Group ID"] or "",
            ]
        )
    all_values = []
    all_values.append(write_headers)
    all_values.extend(write_values)
    print(f"Writing {len(all_values)} entries to {RANGE_NAME}")
    try:
        request = SHEET.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            insertDataOption="OVERWRITE",
            valueInputOption="USER_ENTERED",
            body={"majorDimension": "ROWS", "values": all_values},
        )
        request.execute()

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    f = open("leap_export.json")
    data = json.load(f)
    write_to_sheet(data["data"])
