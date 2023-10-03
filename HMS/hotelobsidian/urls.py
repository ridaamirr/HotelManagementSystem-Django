from django.urls import path
from . import views
from . import loginfunctions

urlpatterns = [
    path('', views.default, name='default'),
    path('login/',views.login,name='login'),
    path('homepage/', loginfunctions.user_dashboard, name='homepage')
]
