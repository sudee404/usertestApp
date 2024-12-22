from django.urls import path
from .views.user_views import create_user,list_users


urlpatterns = [
    path("create/", create_user, name="create_user"),
    path("list/", list_users, name="list_users"),
]
