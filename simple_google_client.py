import httplib2
import apiclient

from oauth2client.service_account import ServiceAccountCredentials


class GoogleClient:
    def __init__(self, credentials_path: str, table_id: str = ""):
        self._service = GoogleClient.build_service(credentials_path)
        self.main_table_id = table_id

    @staticmethod
    def build_service(credentials_path):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive']
                                                                       )
        http_auth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=http_auth)
        return service

    def get_values(self, spreadsheet_id: str, range: str) -> dict:
        request = self._service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                                range=range)
        response = request.execute()
        return response

    # https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.values.html#append
    def append_values(self, spreadsheet_id: str, range: str,
                      data: dict[str, list[list[str | int | float | bool | None]] | str],
                      value_input_option: str) -> dict:
        request = self._service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                               range=range,
                                                               body=data,
                                                               valueInputOption=value_input_option)
        response = request.execute()
        return response


if __name__ == "__main__":
    import os
    from pprint import pprint

    google_service = GoogleClient(os.getenv("GOOGLE_TOKEN_PATH"))

    test_table_id = "1acz1eBGEBwd_qPvJLLQGzj_wcRek8jrR66ceWUIw0n0"
    # pprint(google_service.get_values(test_table_id, "Sheet1!A1:C4"))

    data_to_append = {
        "majorDimension": "ROWS",
        "values": [
            [
                "codilac", "1999", "black"
            ],
        ],
    }

    pprint(google_service.append_values(test_table_id,
                                        range="Sheet1!A1:C10",
                                        data=data_to_append,
                                        value_input_option="USER_ENTERED"))
