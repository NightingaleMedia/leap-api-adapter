from google.oauth2 import service_account
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1NcBCbzBeQHMusSUQKkBEOqOYpBC_iwbZGeEhwYUf4tM"
RANGE_NAME = "NewMeterAssign!A:L"

creds = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)
service = build("sheets", "v4", credentials=creds)
# instantiate the Sheets API
SHEET = service.spreadsheets()
