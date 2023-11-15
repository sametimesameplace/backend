from django.urls import path
from rest_framework import routers

from apps.user import views


router = routers.SimpleRouter()
router.register("api/v1/user", views.ListUsers)
router.register("api/v1/userprofile", views.UserProfileModelViewSet)
router.register("api/v1/userlanguage", views.UserLanguageViewSet, basename='userlanguage') 
router.register("api/v1/language", views.LanguageViewSet, basename='language') 


urlpatterns = [
    path("api/v1/login", views.UserLoginView.as_view({'post': 'create'}), name="login-token"),
    *router.urls,
]
