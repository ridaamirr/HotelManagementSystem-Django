from django.urls import path
from . import views
from . import loginfunctions
from . import signupfunction

urlpatterns = [
    path('', views.default, name='default'),
    path('admin/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('cataloguelist/', views.cataloguelist, name='cataloguelist'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', loginfunctions.user_dashboard, name='homepage'), 
    path('checkavailabilty/', views.checkavailabilty, name='checkavailabilty'),
    path('admin/branchinformation/', views.branchinformation, name='branchinformation')
]

