
#userprofile/logoservices.py

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from ..models.user_model import User

class UserLogoServiceLayer:
    def __init__(self,model):
        self.model=model


    def upload_logo(self,user_id,logo):
         try:
             user = self.model.objects.get(id=user_id)
             user.profile_logo =logo
             user.save()
             return user
         except ObjectDoesNotExist:
             raise ValueError("User does not exist")
         except Exception as e:
             raise ValidationError(f"Error uploading logo: {str(e)}")
    def get_logo(self,user_id):
        try:
            user =self.model.objects.get(id=user_id)
            return user.logo_url
        except ObjectDoesNotExist:
              raise ValueError("User logo does not exist")

    def delete_logo(self,user_id):
        try:
            user =self.model.objects.get(id=user_id)
            user.profile_logo.delete()
            user.profile_logo = None
            user.save()
            return  True
        except ObjectDoesNotExist:
            raise ValueError("user logo does not exist")
        except Exception as e:
            raise ValidationError(f"Error deleting logo:{str(e)}")





