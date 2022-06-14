from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from cars.models import Cars
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
    # product = get_object_or_404(Product, pk=id)
    product = get_object_or_404(Cars, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
        
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product.car_model,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        # success_url=request.build_absolute_uri(
        #     reverse('success')
        # ) + "?session_id={CHECKOUT_SESSION_ID}",
        # cancel_url=request.build_absolute_uri(reverse('failed')),

        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
    )

    
    return JsonResponse({'sessionId': checkout_session.id})


