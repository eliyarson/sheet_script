import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

#originKey = '1G5CrpUKkn5H2tA2IvIYjyIASr3UMoGqo4yXBbX7PtHI'
#originSheetName = 'origin_sheet'
#destinySheetName = 'benchmark_sheet'


def sheet_script(request):
    ## Auth
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )
    gc = gspread.authorize(credentials)

    ## POST Request

    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'origin_key' and 'origin_sheet_name' and 'destiny_sheet_name' in request_json:
            origin_key = request_json['origin_key']
            origin_sheet_name = request_json['origin_sheet_name']
            destiny_sheet_name = request_json['destiny_sheet_name']
            destiny_key = request_json['destiny_key']
        else:
            raise ValueError(
                    "JSON is invalid")
    else:
        raise KeyError("Content type <> application/json")

    ## Open origin_key Spreadsheet
    origin_spreadsheet = gc.open_by_key(origin_key)
    ## Get origin_sheet_name data
    origin_sheet = origin_spreadsheet.worksheet(origin_sheet_name)
    origin_sheet_data = origin_sheet.get_all_values()

    ## Transform into DataFrame for manipulations
    ##uncomment if you want to do data transformation

    #header = origin_sheet_data[0]
    #df = pd.DataFrame(data=origin_sheet_data, columns=header)
    #df.drop(0, inplace=True)
    #df['d'] = [1, 2, 3]
    #rand = list(np.random.randint(0, 10, size=(1000, 4)))
    #df2 = pd.DataFrame(rand, columns=list('abcd'))
    #df = df.append(df2, ignore_index=True)
    #df_list = [df.columns.values.tolist()] + df.values.tolist()

    ## Copy data
    destiny_spreadsheet = gc.open_by_key(destiny_key)
    destiny_sheet = destiny_spreadsheet.worksheet(destiny_sheet_name)
    destiny_sheet.clear()

    #if you uncomment the section above, comment the line below.
    df_list = origin_sheet_data

    rows = len(df_list)
    cols = len(df_list[0])
    destiny_sheet.resize(rows, cols)
    params = {'valueInputOption': 'RAW'}
    body = {'values': df_list}
    destiny_spreadsheet.values_append(f'{destiny_sheet_name}!A1', params, body)
    request_json['status'] = 'OK'

    return request_json
