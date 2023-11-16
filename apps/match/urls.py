from django.urls import path

from rest_framework import routers

from apps.match import views

router = routers.SimpleRouter()

router.register("api/v1/match", views.MatchViewSet)


urlpatterns = [
    *router.urls,
]
