"""
URL configuration for find_shop_near_me project.

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
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shops/', views.shop_list, name='shop_list'),
    path('shops/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('shops/create/', views.shop_create, name='shop_create'),
    path('shops/<int:shop_id>/update/', views.shop_update, name='shop_update'),
    path('shops/<int:shop_id>/delete/', views.shop_delete, name='shop_delete'),
    path('shops/find_nearest/', views.shop_within_distance, name='shop_within_distance'),
]
