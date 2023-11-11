"""
URL configuration for cross_site_ec project.

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
from django.contrib import admin
from django.urls import path
#import cross_site_ec.serch.views.serch_view as serch_views
#import cross_site_ec.serch.views.home_view as home_views
import serch.views.serch_view as serch_views
import serch.views.home_view as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('serch/', serch_views.serchView.as_view()),
    path('home/', home_views.homeView.as_view()),
]
