#views/user_views.py
import json
from django.http import JsonResponse,QueryDict
from django.views.decorators.csrf import csrf_exempt
from ..services.user_service import create_user_service, list_users_service,login_user_service
from django.contrib.auth import authenticate
from ..services.service_layer import ServiceLayer
#from django.contrib.auth.models import User
from ..models.user_model import User
from ..common.validators import unpack_data,missing_required_fields

@csrf_exempt
def create_user(request):
    try:
        data = unpack_data(request)
        print(f"Data is Received: {data}")
        required_fields = ['username', 'email', 'password']
        missing_fields = missing_required_fields(data, required_fields)
        
        #if missing fields, return an error
        if missing_fields:
            return JsonResponse({'error': f'Missing required fields: {missing_fields}'}, status=400)
        print(f"Data is Received: {data}")
        #user = create_user_service(data)
        user = ServiceLayer(model=User).create_user(**data)
        user_data = {
            'id':str(user.id),
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        print(f"User created: {user_data}")
        return JsonResponse(user_data, status=201)
    except Exception as e:
        print(f"Error in create_user: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
#list all users

@csrf_exempt
def list_users(request):

    try:
        user_data =list(ServiceLayer(model=User).all().values('username', 'email', 'created_at', 'updated_at'))

       # user_data = [{
       #     'id': str(user.id),
       #     'username': user.username,
       #     'email': user.email,
       #     'created_at': user.created_at,
       #     'updated_at': user.updated_at
       # } for user in users]
        print(f"Usernames: {[user['username'] for user in user_data]}")#print usernames to console
        return JsonResponse(user_data, safe=False, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#login user
@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        # Debugging import issues
        print(f"Authenticate function: {authenticate}")

        # Process login
        data = unpack_data(request)
        username_or_email = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username_or_email, password=password)
        if not user:
            print(f"Authentication failed for user: {username_or_email}")
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        print(f"User: {user} logged in successfully")
        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        return JsonResponse({'error': str(e)}, status=500)