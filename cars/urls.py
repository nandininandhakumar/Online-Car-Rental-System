
from re import template
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

    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
    path('detail/<id>/', CarDetailView.as_view(), name='detail'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('canel/', PaymentFailedView.as_view(), name='cancel'),
]