from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import jwt
from datetime import datetime, timedelta


def create_auth_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1), # token will expire in 1 hour
        'iat': datetime.utcnow()
    }
    secret = 'your_secret_key_here'
    token = jwt.encode(payload, secret, algorithm='HS256')
    print(token.decode('utf-8'))
    return token.decode('utf-8')



def register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')
        if not all([username, email, password]):
            return JsonResponse({'msg': 'Please fill all fields'}, status=400)
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return JsonResponse({'msg': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400) 
    else:
        return JsonResponse({"msg": "Method not allowed"}, status=400)
    

def logout_view(request):
    logout(request)
    return JsonResponse({'msg': 'Logout successful'})


def login_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username')
        password = body.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({'msg': 'Login successful', 'user_id': user.id, "success": True}, status=200)
            response.set_cookie('auth_token', create_auth_token(user.id), httponly=True, secure=False, samesite='None')    
            return response 
        else:
            return JsonResponse({'msg': 'Invalid credentials'}, status=400)
    else:
        errors = "An error occurred"
        return JsonResponse({'msg': 'Invalid form data', 'errors': errors}, status=400)

        