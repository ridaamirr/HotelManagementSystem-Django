from django.contrib import admin
from django.urls import path
from HMSapp import views

urlpatterns = [
    path('',views.display_table,name='homepage')
]