from django.urls import path
from .views import *

urlpatterns = [
    

    path('checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
]