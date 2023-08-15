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


api_urlpatterns = [
    path("", include("the_factory_bot_task.users.urls")),
    path("", include("the_factory_bot_task.messages.urls")),
]
handler404 = "the_factory_bot_task.views.handler404"
urlpatterns = [path("api/", include(api_urlpatterns))]
