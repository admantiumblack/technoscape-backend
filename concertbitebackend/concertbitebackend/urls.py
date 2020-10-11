"""concertbitebackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from concertbite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/username=<str:username>&password=<str:password>/', views.login),
    path('auth/logout/', views.logout),
    path('auth/register/username=<str:username>&password=<str:password>&email=<str:email>&fullname=<str:fullname>/', views.registerUser),
    path('auth/update/<str:args>/', views.update),
    path('user/data/<str:args>/', views.getData),
]
