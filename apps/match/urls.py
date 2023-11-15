from django.urls import path

from rest_framework import routers

from apps.match import views

router = routers.SimpleRouter()

router.register("api/v1/match", views.MatchViewSet)
router.register("api/v1/matchchat", views.MatchChatViewSet)


urlpatterns = [
    *router.urls,
]
