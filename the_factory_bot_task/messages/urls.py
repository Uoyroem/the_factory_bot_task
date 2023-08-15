from rest_framework.routers import DefaultRouter
from . import views


default_router = DefaultRouter()
default_router.register("messages", views.MessageViewSet, "message")
default_router.register("tokens", views.TokenViewSet, "token")

urlpatterns = default_router.urls
