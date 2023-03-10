"""homework_30_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from advertisements import views
from advertisements.views import CategoryViewSet
from homework_30_2 import settings
from users.views import LocationViewSet

location_router = SimpleRouter()
location_router.register("location", LocationViewSet)

category_router = SimpleRouter()
category_router.register("cat", CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_main_page),
    path('ad/', include("advertisements.urls.advertisements")),
    path('user/', include("users.urls.users")),
    path('api-auth/', include("rest_framework.urls")),
    path('selection/', include("advertisements.urls.selections")),
]

urlpatterns += location_router.urls
urlpatterns += category_router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
