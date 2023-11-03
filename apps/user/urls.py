from django.urls import path
from rest_framework import routers

from apps.user import views

router = routers.SimpleRouter()
router.register("api/v1/user", views.ListUsers)


urlpatterns = [
    *router.urls,
]
