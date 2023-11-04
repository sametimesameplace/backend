from django.urls import path
from rest_framework import routers

from apps.timeplace import views


router = routers.SimpleRouter()
router.register("api/v1/interest", views.InterestViewSet)
router.register("api/v1/activity", views.ActivityViewSet)
router.register("api/v1/timeplace", views.TimePlaceViewSet)

urlpatterns = [
    *router.urls,
]
