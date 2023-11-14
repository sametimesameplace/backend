from django.urls import path
from rest_framework import routers

from apps.user import views
from apps.user.views import UserLoginView

router = routers.SimpleRouter()
router.register("api/v1/user", views.ListUsers)
router.register("api/v1/userprofile", views.UserProfileModelViewSet)


urlpatterns = [
    path("api/v1/login", UserLoginView.as_view({'post': 'create'}), name="login-token"),
    *router.urls,
]
