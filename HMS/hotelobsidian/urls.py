from django.urls import path
from . import views ,generatebillviews,catalogueviews,bookinginfoviews,customerviews,paymentinfoviews, roominformationviews
from .branchviews import(
    BranchInformationAddView,
    BranchInformationUpdateView,
    DeleteBranchView,
    UpdateBranchView,
)
from .roomviews import RoomtypeAddView, RoomtypeUpdateView, DeleteRoomtypeView, UpdateRoomtypeView
from . import loginfunctions
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.default, name='default'),
    path('admin/', views.admin, name='admin'),
    path('login/', views.login, name='login'),
    path('logout',views.logout,name='logout'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', loginfunctions.user_dashboard, name='homepage'), 
    path('checkavailabilty/', views.checkavailabilty, name='checkavailabilty'),

    #Catalogue Links--------------------------------------------------------------------
    path('catalogue/', catalogueviews.catalogue, name='catalogue'),
    path('cataloguelist/', catalogueviews.cataloguelist, name='cataloguelist'),
    path('booking/<int:roomid>/<str:loc>/', catalogueviews.booking, name='booking'), 
    path('booking_final/',catalogueviews.booking_final, name='booking_final'),
    #-----------------------------------------------------------------------------------
    
    #GenerateBill Links------------------------------------------------------------------
    path('generatebill/', generatebillviews.generate_bill, name='generate_bill'),
    path('checkout_Room/<int:roomid>/', generatebillviews.checkout_Room, name='checkout_Room'), 
    path('checkoutAll/',generatebillviews.checkoutAll, name='checkoutAll'), 
    #-----------------------------------------------------------------------------------

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
    path('admin/branchinformation/add_new/', BranchInformationAddView.as_view(), name='add_new_branch'),
    path('admin/branchinformation/new_update/', BranchInformationUpdateView.as_view(), name='update_this_branch'),
    path('delete_branch/<int:branch_id>/', DeleteBranchView.as_view(), name='delete_branch'),
    path('update_branch/<int:branch_id>/', UpdateBranchView.as_view(), name='update_branch'),
    #-----------------------------------------------------------------------------------

    # Room Information Links -----------------------------------------------------------
    path('admin/roominformation/update/', views.roominformation, name='roominformation_update'),
    path('admin/roominformation/add/', views.roominformation, name='roominformation_add'),
    path('admin/roominformation/add_new/', roominformationviews.roominformation_add, name='add_new_roominformation'),
    path('admin/roominformation/add_new_information/<int:room_type_id>/', roominformationviews.roominformation_add_new, name='add_new_roominformation_form'),
    path('admin/roominformation/enter_data/', roominformationviews.roominformation_enter_data, name='enter_data'),
    path('admin/roominformation/new_update/', roominformationviews.roominformation_update, name='update_this_roominformation'),
    path('delete_roominformation/<int:room_id>/', roominformationviews.delete_roominformation, name='delete_roominformation'),
    path('update_roominformation/<int:room_id>/', roominformationviews.update_roominformation, name='update_roominformation'),
    #----------------------------------------------------------------------------------- 

    # Room Type Links -----------------------------------------------------------------
    path('admin/roomtype/update/', views.roomtype, name='room_update'),
    path('admin/roomtype/add/', views.roomtype, name='room_add'),
    path('admin/roomtype/add_new/', RoomtypeAddView.as_view(), name='add_new_room'),
    path('admin/roomtype/new_update/', RoomtypeUpdateView.as_view(), name='update_this_room'),
    path('delete_roomtype/<int:roomtype_id>/', DeleteRoomtypeView.as_view(), name='delete_room'),
    path('update_roomtype/<int:roomtype_id>/', UpdateRoomtypeView.as_view(), name='update_room'),
    #-----------------------------------------------------------------------------------

    # Booking Information Links ---------------------------------------------------------
    path('admin/bookinginformation/checkoutroom/<int:roomid>/', bookinginfoviews.checkout_Room_byadmin, name='checkout_Room_byadmin'),path('admin/bookinginformation/checkoutroom/<int:roomid>/', bookinginfoviews.checkout_Room_byadmin, name='checkout_Room_byadmin'),
    path('admin/bookinginformation/bookings_search', bookinginfoviews.bookings_search, name='bookings_search'),
    #----------------------------------------------------------------------------------- 

    # Customer Information Links ---------------------------------------------------------  
    path('admin/customerinformation/customer_search', customerviews.customer_search, name='customer_search'),
    #------------------------------------------------------------------------------------- 

    #Payment Views------------------------------------------------------------------------  
    path('admin/payments/payments_search', paymentinfoviews.payments_search, name='payments_search'),
    path('admin/payments/paid/<str:id>/', paymentinfoviews.paid, name='paid'), 

    #BillDetails--------------------------------------------------------------------------
    path('admin/billdetails/<str:id>/', paymentinfoviews.billdetails, name='billdetails'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)