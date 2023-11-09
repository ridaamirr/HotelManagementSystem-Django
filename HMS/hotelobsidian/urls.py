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
    path('logout',views.logout,name='logout'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('cataloguelist/', views.cataloguelist, name='cataloguelist'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', loginfunctions.user_dashboard, name='homepage'),
    path('booking/<int:roomid>/<str:loc>/', views.booking, name='booking'), 
    path('booking_final/', views.booking_final, name='booking_final'),
    path('checkavailabilty/', views.checkavailabilty, name='checkavailabilty'),
    path('generatebill/', views.generate_bill, name='generate_bill'),
    path('admin/branchinformation/', views.branchinformation, name='branchinformation')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)