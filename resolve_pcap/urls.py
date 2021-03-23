"""resolve_pcap URL Configuration

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
from django.urls import path
from app import views
from django.views.generic import TemplateView
urlpatterns = [
    path('',TemplateView.as_view(template_name='index.html')),
    path('api/uploadpcapfile/', views.resove_pcapfile),
    path('api/getpackages/<int:fileid>/<str:proto>/<str:source>/<str:target>/',views.getpackages),
    path('api/gettestdata/<int:fileid>/', views.gettestdata),
    path('api/getdetail/<int:fileid>/<int:ind>/',views.getdetail),
    path('api/getpackagesbaseonsrc/<int:fileid>/<str:source>/',views.getpackagesbaseonsrc),
]
