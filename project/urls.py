"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #1
    path('django/jsonresponsemodel/',views.no_rest_no_model),
    
    #2
    path('django/jsonresponsefrommodel/',views.no_rest_from_model),
    
    #3 GET POST from rest framework Function Based View @api_view
    path('list/fbv/',views.FBV_list),
    
    
    #4 GET PUT DELETE from rest framework function based view @api_view
    path('list/fbv/<int:pk>/',views.FBV_pk),


]
