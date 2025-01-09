import json
from django.http import JsonResponse
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
            is_superuser = data.get('is_superuser', False)
            print(f"Data received in create_user: {data}")

            if is_superuser:
                print(f"Superuser created: {data.get('email')}")

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
                print("Missing email or password in login_user")
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            user = authenticate(username=email, password=password)
            if not user:
                print(f"Authentication failed for: {email}")
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

            # Check if user is superuser
            is_superuser = user.is_superuser
            print(f"User logged in successfully: {user.username}")
            return JsonResponse({'status': 'success', 'username': user.username, 'is_superuser': is_superuser}, status=200)
        except Exception as e:
            print(f"Unexpected error in login_user: {str(e)}")
            return JsonResponse({'error': f"Error occurred during login: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def assign_role(request):
    if request.method == "POST":
        try:
            data = unpack_data(request)
            user_id = data.get('user_id')
            role_group_name = data.get('role_group_name')
            requester = request.user  # Assuming the requester is the authenticated user

            if not user_id or not role_group_name:
                return JsonResponse({'error': 'user_id and role_group_name are required'}, status=400)

            user_service = UserService()
            result = user_service.assign_role(user_id, role_group_name, requester)

            return JsonResponse(result, status=200)
        except ValidationError as ve:
            print(f"Validation error in assign_role: {str(ve)}")
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            print(f"Error in assign_role: {str(e)}")
            return JsonResponse({'error': f"Error occurred during role assignment: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
