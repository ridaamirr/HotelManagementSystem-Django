from django.urls import path
from . import views
from . import loginfunctions
from . import signupfunction
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.default, name='default'),
    path('admin/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('cataloguelist/', views.cataloguelist, name='cataloguelist'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', loginfunctions.user_dashboard, name='homepage'),
    path('booking/', views.booking, name='booking'),
    path('checkavailabilty/', views.checkavailabilty, name='checkavailabilty'),
    path('admin/branchinformation/', views.branchinformation, name='branchinformation')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)