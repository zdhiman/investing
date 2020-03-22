import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def create_service(
    client_secret_file="specifications/credentials.json",
    api_service_name="sheets",
    api_version="v4",
    scope="https://www.googleapis.com/auth/spreadsheets",
):
    global service

    cred = None

    if os.path.exists("token_write.pickle"):
        with open("token_write.pickle", "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scope)
            cred = flow.run_local_server()

        with open("token_write.pickle", "wb") as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, "service created!")
    except Exception as e:
        print(e)


def export_df_to_sheets(df, sheet_id, cell_range):
    create_service()
    response_date = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=sheet_id,
            valueInputOption="RAW",
            range=cell_range,
            body=dict(
                majorDimension="ROWS", values=df.T.reset_index().T.values.tolist()
            ),
        )
        .execute()
    )
    print("sheet updated!")
