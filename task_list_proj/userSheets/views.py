from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from googleSheets.models import Sheet
from django.contrib.auth.models import User


def get_user_sheets(request, user_id):
    print("Getting user sheets")
    #if not request.user.is_authenticated:
     #   return JsonResponse({'error': 'You must be logged in to create a sheet'})
    
    print(f"The user ID is {user_id}")

    sheets = Sheet.objects.filter(user_id=user_id)
    if not sheets:
        return JsonResponse({'error': 'No sheets found for this user'})
    
    query_set = list(map(lambda x: x.serialize(), sheets))
    return JsonResponse(query_set, safe=False)

def get_sheet_by_id(request,user_id,sheet_id):
   # if not request.user.is_authenticated:
   #     return JsonResponse({'error': 'You must be logged in to create a sheet'})
    
    print(f"The user ID is {user_id}")
    print(f"The sheet ID is {sheet_id}")

    sheet = Sheet.objects.filter(user_id=user_id).filter(sheet_id=sheet_id)
    if not sheet:
        return JsonResponse({'error': 'No sheets found for this user'})
    
    query_set = list(map(lambda x: x.serialize(), sheet))
    return JsonResponse(query_set, safe=False)
    