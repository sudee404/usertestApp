import json
from django.http import JsonResponse,QueryDict
from django.views.decorators.csrf import csrf_exempt
from ..services.user_service import create_user_service


def unpack_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    elif request.method == 'GET':
        data = request.GET
    else:
        data = {}
    return data
def missing_required_fields(data, required_fields):
    missing_fields = []
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
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        return JsonResponse(user_data, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)