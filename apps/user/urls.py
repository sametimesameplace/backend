from django.urls import path
from apps.user import views


urlpatterns = [
    path("list/", views.user_list, name="user-list"),
]
