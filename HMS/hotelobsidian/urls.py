from django.urls import path
from . import views, branchviews
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
    path('checkout_Room/<int:roomid>/', views.checkout_Room, name='checkout_Room'), 
    path('checkoutAll/', views.checkoutAll, name='checkoutAll'),

    #Admin Dashboard Links -------------------------------------------------------------
    path('admin/branchinformation/', views.branchinformation, name='branchinformation'),
    path('admin/roomtype/', views.roomtype, name='roomtype'),
    path('admin/roominformation/', views.roominformation, name='roominformation'),
    path('admin/customerinformation/',views.customerinformation, name='customerinformation'),
    path('admin/bookinginformation/',views.bookinginformation, name='bookinginformation'),
    path('admin/payments/',views.payments, name='payments'),
    #-----------------------------------------------------------------------------------

    # Branch Information Links ---------------------------------------------------------
    path('admin/branchinformation/update/', views.branchinformation, name='branch_update'),
    path('admin/branchinformation/add/', views.branchinformation, name='branch_add'),
    path('admin/branchinformation/add_new/', branchviews.branchinformation_add, name='add_new_branch'),
    path('admin/branchinformation/new_update/', branchviews.branchinformation_update, name='update_this_branch'),
    path('delete_branch/<int:branch_id>/', branchviews.delete_branch, name='delete_branch'),
    path('update_branch/<int:branch_id>/', branchviews.update_branch, name='update_branch'),
    path('sample/', views.sample_view, name='sample_view'),
    #-----------------------------------------------------------------------------------
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)