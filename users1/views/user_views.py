import json
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from ..services.user_service import UserService
from ..services.service_layer import ServiceLayer
from ..models.user_model import User
from ..common.validators import unpack_data, missing_required_fields
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        try:
            data = unpack_data(request)
            print(f"Data received in create_user: {data}")

            required_fields = ['username', 'email', 'password']
            missing_fields = missing_required_fields(data, required_fields)

            if missing_fields:
                print(f"Missing fields in create_user: {missing_fields}")
                return JsonResponse({'error': f"Missing required fields: {missing_fields}"}, status=400)

            user_service = UserService()
            user_data = user_service.create_user(data)

            print(f"User created: {user_data}")
            return JsonResponse(user_data, status=201)
        except ValidationError as ve:
            print(f"Validation error in create_user: {str(ve)}")
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            print(f"Error in create_user: {str(e)}")
            return JsonResponse({'error': f"Error occurred during user creation: {str(e)}"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def list_users(request):
    if request.method == "GET":
        try:
            filters = request.GET.dict()  # Extract filters from QueryDict
            print(f"Filters received in list_users: {filters}")

            user_data = list(ServiceLayer(model=User).filter(**filters).values(
                'username', 'email', 'created_at', 'updated_at'
            ))
            print(f"Users retrieved: {user_data}")
            return JsonResponse(user_data, safe=False, status=200)
        except Exception as e:
            print(f"Error in list_users: {str(e)}")
            return JsonResponse({'error': f"Error occurred while fetching users: {str(e)}"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = unpack_data(request)
            print(f"Data received in login_user: {data}")

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                print("Missing username or password in login_user")
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            user = authenticate(username=email, password=password)
            if not user:
                print(f"Authentication failed for: {email}")
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

            print(f"User authenticated: {user.username}")
            return JsonResponse({'status': 'success', 'username': user.username}, status=200)
        except Exception as e:
            print(f"Unexpected error in login_user: {str(e)}")
            return JsonResponse({'error': f"Error occurred during login: {str(e)}"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
