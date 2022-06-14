

from django.urls import path

from .views import *

urlpatterns = [
    path('',Index.as_view(),name="index" ),
    path('registraion/',Registration.as_view(),name="cars/registration/registration"),
    path('login/',Login.as_view(),name="cars/registration/login"),
    path('customer_index/',Customer_index.as_view(),name="cars/customer/customer_index"),
    path('owner_index/',Owner_index.as_view(),name="cars/carshop_owner/owner_index"),
    path('add_car/',Add_car.as_view(),name="cars/carshop_owner/add_car"),
    path('edit_car/<int:id>/',Edit_car.as_view(),name="cars/cashop_owner/edit_car"),
    path('delete_car/<int:id>',Delete_car.as_view(),name="cars/cashop_owner/delete_car"),
    path('book_car/',Book_car.as_view(),name="cars/customer/book_car"),
    path('logout/',Logout.as_view(),name="logout"),

    
    path('detail/<id>/', CarDetailView.as_view(), name='detail'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('canel/', PaymentFailedView.as_view(), name='cancel'),


    path('auth/settings', settings, name='settings'),
    path('home_sub', home, name='home_sub'),
    path('join', join, name='join'),
    path('checkout', checkout, name='checkout'),
    path('deletemsg',Deletemsg,name="deletemsg"),
    path('pausemsg',Pausemsg,name="pausemsg"),
    path('resumemsg',Resumemsg,name="resumemsg"),
    path('pausepayment',Pausepayment, name="pausepayment"),
    path('resumepayment',Resumepayment, name="resumepayment"),

    path('upgrademsg',Upgrademsg,name="upgrademsg"),
    path('upgrade',Upgrade, name="upgrade"),

    path('downgrade',Downgrade, name="downgrade"),

    path('deletesubscription',Deletesubscription, name="deletesubscription"),
    path('success_sub', success, name='success_sub'),
    path('cancel_sub', cancel, name='cancel_sub'),
    path('updateaccounts', updateaccounts, name='updateaccounts'),
]