from script.config import SHEET


def add_created_group_to_sheet(
    group,
    created_group_id,
    created_group_name,
    SPREADSHEET_ID="1NcBCbzBeQHMusSUQKkBEOqOYpBC_iwbZGeEhwYUf4tM",
    RANGE="CreatedExports!A:AAZ",
):

    write_values = []
    write_values.append(
        [
            group["MeterId"],
            group["OldPartnerRef"],
            group["NewPartnerRef"],
            group["Zen Org ID"],
            group["Zen Org Name"],
            group["Zen Region ID"],
            created_group_id,
            created_group_name,
            group["Utility"],
            group["Customer"],
            group["ServiceAddress"],
            group["input_data"]["location"]["address"],
            group["Status"],
        ]
    )

    try:
        request = SHEET.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE,
            insertDataOption="OVERWRITE",
            valueInputOption="USER_ENTERED",
            body={"majorDimension": "ROWS", "values": write_values},
        )
        request.execute()

    except HttpError as err:
        print(err)
