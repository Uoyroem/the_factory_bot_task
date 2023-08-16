"""
URL configuration for the_factory_bot_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from .users.views import UserReadOnlyViewSet
from .messages.views import MessageViewSet, TokenViewSet
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _


default_router = routers.DefaultRouter()
default_router.register("users", UserReadOnlyViewSet, "user")
default_router.register("messages", MessageViewSet, "message")
default_router.register("tokens", TokenViewSet, "token")


@api_view()
def handler404(request: Request, exception: Exception) -> Response:
    raise NotFound


urlpatterns = [path("api/", include(default_router.urls))]
