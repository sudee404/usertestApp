#userprofile/profile_views.py
from .logoservices import UserLogoServiceLayer
from ..models import User
from ..common.validators import unpack_data
from django.http import JsonResponse
import json
from  django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_logo(request):
    if request.method == "POST":
        try:
            user_id = request.user.id
            logo = request.FILES.get('logo')
            
            if not logo:
                print("No logo file provided")
                return JsonResponse({'error': 'No logo file provided'}, status=400)
            
            logo_service = UserLogoServiceLayer(User)
            user = logo_service.upload_logo(user_id, logo)
            
            print(f"Logo uploaded for user: {user.username}")
            return JsonResponse({
                'message': 'Logo uploaded successfully',
                'logo_url': user.logo_url
            }, status=201)
            
        except Exception as e:
            print(f"Error in upload_logo: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_logo(request):
    if request.method == "GET":
        try:
            user_id = request.user.id
            logo_service = UserLogoServiceLayer(User)
            logo_url = logo_service.get_logo(user_id)
            
            print(f"Logo retrieved for user ID: {user_id}")
            return JsonResponse({'logo_url': logo_url}, status=200)
            
        except Exception as e:
            print(f"Error in get_logo: {str(e)}")
            return JsonResponse({'error': str(e)}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_logo(request):
    if request.method == "DELETE":
        try:
            user_id = request.user.id
            logo_service = UserLogoServiceLayer(User)
            logo_service.delete_logo(user_id)
            
            print(f"Logo deleted for user ID: {user_id}")
            return JsonResponse({'message': 'Logo deleted successfully'}, status=200)
            
        except Exception as e:
            print(f"Error in delete_logo: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)