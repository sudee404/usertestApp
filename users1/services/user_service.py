from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from ..common.validators import missing_required_fields
from ..models.user_model import User


class UserService:
    def __init__(self):
        self.model = User

    def create_user(self, data):
        """Create a new user and return user details along with token."""
        required_fields = ['username', 'email', 'password']
        missing_fields = missing_required_fields(data, required_fields)

        if missing_fields:
            raise ValidationError(f"Missing required fields: {missing_fields}")

        # Extract the is_superuser field, defaulting to False
        is_superuser = data.get('is_superuser', False)

        # Create the user
        user = self.model.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # Set the is_superuser attribute
        user.is_superuser = is_superuser
        user.save()

        # Create or get the token for the user
        token, created = Token.objects.get_or_create(user=user)

        return {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'token': token.key,
            'is_superuser': user.is_superuser  # Include is_superuser in the response
        }

    def login_user(self, data):
        """Authenticate user and return user details along with token."""
        required_fields = ['email', 'password']
        missing_fields = missing_required_fields(data, required_fields)

        if missing_fields:
            raise ValidationError(f"Missing login required fields: {missing_fields}")

        email = data['email']
        password = data['password']

        # Authenticate user with email as username
        user = authenticate(username=email, password=password)
        if not user:
            raise ValidationError("Invalid email or password")

        if not user.is_active:
            raise ValidationError("Account is deactivated")

        token, created = Token.objects.get_or_create(user=user)

        return {
            'username': user.username,
            'email': user.email,
            'token': token.key
        }

    def list_users(self):
        """Retrieve a list of all users."""
        return list(self.model.objects.values('id', 'username', 'email', 'date_joined'))

    def assign_role(self, user_id, role_group_name, requester):
        """Assign a role to a user, only accessible by superusers."""
        if not requester.is_superuser:
            raise ValidationError("Only superusers can assign roles.")
        try:
            user = self.model.objects.get(id=user_id)
            group, created = Group.objects.get_or_create(name=role_group_name)
            group.user_set.add(user)
            return {
                'message': f"Role {role_group_name} assigned to user {user.username} successfully"
            }
        except self.model.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} not found.")
        except Exception as e:
            raise ValidationError(f"Error assigning role: {str(e)}")
