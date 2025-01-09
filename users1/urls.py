from django.urls import path
from .views.user_views import create_user,list_users,login_user
from .userprofile.profile_views import upload_logo,get_logo,delete_logo


urlpatterns = [
    path("create/", create_user, name="create_user"),
    path("list/", list_users, name="list_users"),
    path("login/", login_user, name="login_user"),
    path("upload_logo/", upload_logo, name="upload_logo"),
    path("get_logo/", get_logo, name="get_logo"),
    path("delete_logo/", delete_logo, name="delete_logo"),
]
