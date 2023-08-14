from rest_framework import routers
from django.urls import include, path

from . import views


default_router = routers.DefaultRouter()
default_router.register("users", views.UserReadOnlyViewSet, "user")

urlpatterns = default_router.urls
