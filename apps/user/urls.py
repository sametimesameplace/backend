from django.urls import path
from rest_framework import routers

from apps.user import views

router = routers.SimpleRouter()
router.register("api/v1/user", views.ListUsers)
router.register("api/v1/userprofile", views.UserProfileModelViewSet)


urlpatterns = [
    path("api/v1/login", views.UserLoginView.as_view(), name="login-token"),
    *router.urls,
]
