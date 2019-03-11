"""whoismrsaemir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter
from .views import DomainsViewSet, run_task, refresh_queue, check_queue

router = DefaultRouter()
router.register(r'', DomainsViewSet, base_name='domain')


urlpatterns = [
    re_path('^check_queue/$', check_queue),
    re_path(r'^refresh_queue/$', refresh_queue),
    re_path(r'^run_task/$', run_task),
    re_path(r'', include(router.urls)),
]
