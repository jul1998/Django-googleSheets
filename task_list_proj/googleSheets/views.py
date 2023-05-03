from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
import os.path
import json
from django.contrib.auth.decorators import login_required

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth.exceptions
from .models import Sheet
from django.contrib.auth.models import User


SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']



def get_credentials():
    credentials = None
    if 'token.json' in os.listdir():
        credentials = Credentials.from_authorized_user_file(
            'token.json', SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    # Always refresh credentials before returning
    credentials.refresh(Request())
    return credentials


def create_sheet(request):
    #if not request.user.is_authenticated:
    #    return JsonResponse({'error': 'You must be logged in to create a sheet'})
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    sheet_name = body["sheet_name"]
    user_id = body["user_id"]


    user = User.objects.get(id=user_id)
    print(user)

    #delete the token file to force getting new credentials
    #if 'token.json' in os.listdir():
        #os.remove('token.json')

    credentials = get_credentials()

    # Create the new sheet
    try:
        service = build('sheets', 'v4', credentials=credentials)

        spreadsheet = service.spreadsheets().create(body={
            'properties': {'title': sheet_name},
            'sheets': [{'properties': {'title': 'Sheet1'}}],
        }).execute()
    except HttpError as e:
        return JsonResponse({'error': str(e)})

    # Return the new sheet ID to the client
    new_sheet = Sheet(
        sheet_id=spreadsheet['spreadsheetId'], sheet_name=sheet_name, user=user)
    new_sheet.save()
    return JsonResponse({"success":True ,'sheet_id': spreadsheet['spreadsheetId']}, status=200)


def get_values(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    spreadsheet_id = body.get('spreadsheet_id')
    range_name = body.get('range_name')

    credentials = get_credentials()

    try:
        service = build('sheets', 'v4', credentials=credentials)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        return JsonResponse({'rows': rows})
    except HttpError as error:
        print(f"An error occurred: {error}")
        return JsonResponse({'error': str(error)})


def batch_get_values(request):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    spreadsheet_id = body.get("spreadsheet_id")
    range_names = body.get("range_names").split(",")  # e.g. "A1:B2,A1:B2"

    credentials = get_credentials()

    try:
        service = build("sheets", "v4", credentials=credentials)
        result = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id, ranges=range_names
        ).execute()
        rows = result.get("valueRanges", [])
        print(f"{len(rows)} rows retrieved")
        return JsonResponse({"rows": rows})
    except HttpError as error:
        print(f"An error has occurred: {error}")
        return JsonResponse({"error": str(error)})


def update_values(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    spreadsheet_id = body.get('spreadsheet_id')
    range_name = body.get('range_name')
    values = body.get('values')
    value_input_option = body.get('value_input_option')

    credentials = get_credentials()

    try:
        service = build('sheets', 'v4', credentials=credentials)

        body = {
            'values': values
        }

      # Split the range_name to get individual ranges
        range_names = range_name.split(',')

        # Perform update operation on each range
        for r in range_names:
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=r,
                valueInputOption=value_input_option, body=body).execute()
            print(f"{result.get('updatedCells')} cells updated in {r}.")

        print(f"{result.get('updatedCells')} cells updated.")
        return JsonResponse({'updated_cells': result.get('updatedCells')})
    except HttpError as error:
        print(f"An error occurred: {error}")
        return JsonResponse({'error': str(error)})


def batch_update_values(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    spreadsheet_id = body.get('spreadsheet_id')
    range_name = body.get('range_name').split(',')  # e.g. "A1:B2,A1:B2"
    values = body.get('values')
    value_input_option = body.get('value_input_option')

    credentials = get_credentials()

    try:
        service = build('sheets', 'v4', credentials=credentials)

        data = []
        for r in range(len(range_name)):
            print(values[r])
            data.append({
                'range': range_name[r],
                'values': values
            })

        body = {
            'valueInputOption': value_input_option,
            'data': data
        }

        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        print(f"{result.get('totalUpdatedCells')} cells updated.")

        return JsonResponse({'updated_cells': result.get('totalUpdatedCells')})
    except HttpError as error:
        print(f"An error occurred: {error}")
        return JsonResponse({'error': str(error)})
    
def delete_sheet(request):
    body_unicode = request.body.decode('utf-8')
    print(body_unicode)
    body = json.loads(body_unicode)
    spreadsheet_id = body.get('spreadsheet_id')
    print(body)

    credentials = get_credentials()

    if request.method == "DELETE":

        try:
            service = build('drive', 'v3', credentials=credentials)

            result = service.files().delete(fileId=spreadsheet_id).execute()
            print(f"Spreadsheet {spreadsheet_id} deleted.")

            sheet_to_delete = Sheet.objects.get(sheet_id=spreadsheet_id)
            sheet_to_delete.delete()
            

            return JsonResponse({'success': True})
        except HttpError as error:
            print(f"An error occurred: {error}")
            return JsonResponse({'error': str(error)})
    else:
        return JsonResponse({'error': 'Invalid request method'})