import json
from googleapiclient.errors import HttpError
from script.call_google import call_google_maps
from script.config import SHEET
from script.write_to_sheet import write_to_sheet

SPREADSHEET_ID = "1fuFt4_R-wH7hoCICOE8MlrpcOeEKlGMKNFS0VVvf_5c"
RANGE_NAME = "MockMeterAssign!A:L"


def main():
    try:

        result = (
            SHEET.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        )
        values: list = result.get("values", [])

        if not values:
            print("No data found.")
            return
        titles = values.pop(0)
        print(titles)
        json_list: list = []
        error_list: list = []
        final_list = []
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

        final_list = call_google_maps(json_list=json_list)
        error_list = filter(lambda item: item["input_data"] is None, final_list)

        json_object = json.dumps(
            dict({"errors": list(error_list), "data": final_list}), indent=4
        )
        # Writing to sample.json
        with open("mock_leap_export.json", "w") as outfile:
            outfile.write(json_object)
            # Print columns A and E, which correspond to indices 0 and 4.
        write_to_sheet(final_list=final_list)
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
