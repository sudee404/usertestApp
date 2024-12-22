from ..models.user_model import User



def create_user_service(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate user data
    if not username or not email or not password:
        raise ValueError('Username, email, and password are required')


        # Create and save user
    user = User.objects.create_user(username=username, email=email, password=password)
    
    return user
