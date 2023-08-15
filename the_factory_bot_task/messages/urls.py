from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views


default_router = DefaultRouter()
default_router.register("messages", views.MessageViewSet, "message")
default_router.register("tokens", views.TokenViewSet, "token")

urlpatterns = default_router.urls
