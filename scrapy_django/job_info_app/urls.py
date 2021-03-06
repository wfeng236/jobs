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
    path('main/', include(([
        path('page/', views.main_page, name='page'),
        path('suggest/', views.suggest_ajax, name="suggest"),
    ],'main'))),

    path('introduce/', views.introduce_page,name='introduce'),
    path('menu/', views.menu_page,name='menu'),
    path('sort/', views.dataSort,name='sort'),
]
