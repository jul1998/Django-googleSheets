from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')
        if not all([username, email, password]):
            return JsonResponse({'error': 'Please fill all fields'})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return JsonResponse({'success': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({"error": "Method not allowed"})
    
def login_view(request):
   if request.method == 'POST':
       data = json.loads(request.body)
       username = data.get('username')
       password = data.get('password')
       
       user = authenticate(request, username=username, password=password)
      
       if user is not None:
           login(request, user)
           return JsonResponse({'success': True, 'message': 'Login successful'})
       else:
           return JsonResponse({'success': False, 'message': 'Invalid credentials'})
   else:
       return JsonResponse({'success': False, 'message': 'Invalid request method'})
   
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})


#def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             print(username, password)
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return JsonResponse({'success': True})
#             else:
#                 return JsonResponse({'success': False, 'message': 'Invalid credentials'})
#         else:
#             errors = form.errors.as_json()
#             return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': errors})
#     else:
#         return JsonRespon