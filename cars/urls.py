from atexit import register
from django.urls import path

from .views import *

urlpatterns = [
    path('',Index.as_view(),name="index" ),
    path('registraion/',Registration.as_view(),name="cars/registration/registration"),
    path('login/',login,name="cars/registration/login"),
    path('customer_index/',customer_index,name="cars/customer/customer_index"),
    path('owner_index/',owner_index,name="cars/carshop_owner/owner_index"),
    path('add_car/',add_car,name="cars/carshop_owner/add_car"),
    path('edit_car/<int:id>',edit_car,name="cars/cashop_owner/edit_car"),
    path('delete_car/<int:id>',delete_car,name="cars/cashop_owner/delete_car"),
    path('book_car/',book_car,name="cars/customer/book_car"),
    path('logout/',logout,name="logout"),
]