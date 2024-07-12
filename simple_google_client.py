import httplib2
import apiclient

from oauth2client.service_account import ServiceAccountCredentials


class GoogleClient:
    def __init__(self, credentials_path: str, table_id: str = ""):
        self.spreadsheet = GoogleClient.build_service(credentials_path)
        self.drive = GoogleClient.build_service(credentials_path, "drive", "v3")
        self.main_table_id = table_id

    @staticmethod
    def build_service(credentials_path, service_name='sheets', api_version='v4'):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive']
                                                                       )
        http_auth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build(service_name, api_version, http=http_auth)
        return service

    def get_values(self, spreadsheet_id: str, range: str) -> dict:
        request = self.spreadsheet.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                               range=range)
        response = request.execute()
        return response

    def add_sheet(self, spreadsheet_id: str, request: dict[str, list[dict[str, dict[str, dict[str, str]]]]]) -> dict:
        request = self.spreadsheet.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                              body=request)

        response = request.execute()
        return response

    # https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.values.html#append
    def append_values(self, spreadsheet_id: str, range: str,
                      data: dict[str, list[list[str | int | float | bool | None]] | str],
                      value_input_option: str) -> dict:
        request = self.spreadsheet.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                                  range=range,
                                                                  body=data,
                                                                  valueInputOption=value_input_option)
        response = request.execute()
        return response


if __name__ == "__main__":
    import os
    from pprint import pprint

    google = GoogleClient(os.getenv("GOOGLE_TOKEN_PATH"))

    file_id = 'your_file_id'

    permissions = google.drive.permissions().list(fileId=file_id).execute()
    pprint(permissions)

    # for permission in permissions.get('permissions', []):
    #     print(f"ID: {permission['id']}, Role: {permission['role']}, Type: {permission['type']}")
    #
    # for permission in permissions.get('permissions', []):
    #     print(f"ID: {permission['id']}")
    #     print(f"Type: {permission['type']}")
    #     print(f"Role: {permission['role']}")
    #     print(f"Email Address: {permission.get('emailAddress', 'N/A')}")
    #     print(f"Domain: {permission.get('domain', 'N/A')}")
    #     print(f"AllowFileDiscovery: {permission.get('allowFileDiscovery', 'N/A')}")
    #     print(f"DisplayName: {permission.get('displayName', 'N/A')}")
    #     print(f"PhotoLink: {permission.get('photoLink', 'N/A')}")
    #     print("------")

    # pprint(google_service.get_values(test_table_id, "Sheet1!A1:C4"))

    # data_to_append = {
    #     "majorDimension": "ROWS",
    #     "values": [
    #         [
    #             "codilac", "1999", "black"
    #         ],
    #     ],
    # }
    #
    # pprint(google_service.append_values(test_table_id,
    #                                     range="Sheet1!A1:C10",
    #                                     data=data_to_append,
    #                                     value_input_option="USER_ENTERED"))

    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets?hl=ru
    # request = {
    #     "requests": [
    #         {
    #             "addSheet": {
    #                 "properties": {
    #                     "sheetId": "777",
    #                     "title": "azino"
    #                 }
    #             }
    #         }
    #     ]
    # }

    # pprint(google_service.add_sheet(test_table_id, request=request))
