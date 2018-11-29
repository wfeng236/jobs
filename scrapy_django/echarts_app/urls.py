"""scrapy_django URL Configuration

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
from django.urls import path, include
from . import views

urlpatterns = [
    path('bar_page/', views.bar_page,name='bar'),
    path('pie_page/', views.pie_page,name='pie'),
    path('map_page/', views.map_page,name='map'),
    path('bar_json/', views.bar_json,name='bar_json'),
    path('pie_json/', views.pie_json,name='pie_json'),
    path('map_json/', views.map_json, name='map_json'),
]
