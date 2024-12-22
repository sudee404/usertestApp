import json
from django.http import JsonResponse,QueryDict
from django.views.decorators.csrf import csrf_exempt
from ..services.user_service import create_user_service, list_users_service


# Unpacks data from request based on HTTP method
def unpack_data(request):
    if request.method == 'POST':
        # For POST requests, parse JSON from request body
        data = json.loads(request.body)
    elif request.method == 'GET':
        # For GET requests, use query parameters
        data = request.GET
    else:
        # For other request methods, return empty dict
        data = {}
    return data

# Checks for missing required fields in the data
def missing_required_fields(data, required_fields):
    missing_fields = []
    # Loop through required fields and check if each exists in data
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    return missing_fields
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
        user = create_user_service(data)
        user_data = {
            'id':str(user.id),
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        return JsonResponse(user_data, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
#list all users

@csrf_exempt
def list_users(request):
    try:
        users = list_users_service()
        user_data = [{
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        } for user in users]
        print(f"Usernames: {[user['username'] for user in user_data]}")#print usernames to console
        return JsonResponse(user_data, safe=False, status=200)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)