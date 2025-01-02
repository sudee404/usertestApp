#services/user_service.py #mywork
from ..models.user_model import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ..common.validators import missing_required_fields
class UserService:
    def __init__(self):
        self.model = User

    def create_user(self,data):
        required_fields =['username','email','password']
        missing_fields = missing_required_fields(data,required_fields) 

        if missing_fields:
            raise ValidationError(f'missing requireds fields:{missing_fields}')   
        return self.model.objects.create_user(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )
    def list_users(self):
        return self.model.objects.all()
    def login_user(self,data):
        required_fields =['username','password']
        missing_fields = missing_required_fields(data,required_fields)

        if missing_fields:
            raise ValidationError (f"missing login required fields:{missing_fields}")
        username_or_email = data['username']
        password = data['password']

        user = authenticate(username=username_or_email,password=password)

        if not user:
            raise ValidationError("Invalid user credentials")
        
        if not user.is_active:
            raise ValidationError("Account is deactivated")
        return user