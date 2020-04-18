import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

#originKey = '1G5CrpUKkn5H2tA2IvIYjyIASr3UMoGqo4yXBbX7PtHI'


def sheet_script(request):
    ## Auth
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    ## POST Request
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'originKey' in request_json:
            originKey = request_json['originKey']
            print(originKey)
        else:
            raise ValueError(
                "JSON is invalid")

    gc = gspread.authorize(credentials)
    ## Open Spreadsheet
    spreadsheet = gc.open_by_key(originKey)
    ## Get sheet data
    sheet = spreadsheet.get_worksheet(0)
    sheet_data = sheet.get_all_values()



    ## Transform into DataFrame for manipulations

    header = sheet_data[0]
    df = pd.DataFrame(data=sheet_data, columns=header)
    df.drop(0, inplace=True)
    df['d'] = [1, 2, 3]
    rand = list(np.random.randint(0, 10, size=(1000, 4)))
    df2 = pd.DataFrame(rand, columns=list('abcd'))
    df = df.append(df2, ignore_index=True)
    df_list = [df.columns.values.tolist()] + df.values.tolist()

    ## Copy data
    sheet_name = 'new_sheet'
    copy_sheet = spreadsheet.worksheet(sheet_name)
    copy_sheet.clear()
    rows = len(df_list)
    cols = len(df_list[0])
    copy_sheet.resize(rows, cols)
    params = {'valueInputOption': 'RAW'}
    body = {'values': df_list}
    spreadsheet.values_append(f'{sheet_name}!A1', params, body)

    return 'OK'
