from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name='default'),
    path('login/',views.login,name='login'),
    path('homepage/',views.user_dashboard, name='homepage')
]
