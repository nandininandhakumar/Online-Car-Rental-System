
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
import stripe
from cars.form import CarsForm
from cars.models import Cars
from django.views import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

from django.views.generic import TemplateView, DeleteView, ListView, UpdateView, DetailView
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class Index(TemplateView):
    template_name = 'cars/index.html'

# This class will register the customer
class Registration(View):
    def get(self, request):
        return render(request,'cars/registration/registration.html')
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is already exist')
                return redirect('cars/registration/registration')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.save()
                messages.info(request, 'customer registered')
                return redirect("cars/registration/login")
        else:
            messages.info(request,'password is not matching')
            return redirect('cars/registration/registration')

# This class is login for admin and customer
class Login(View):
    def get(self, request):
        return render(request,'cars/registration/login.html')
    def post(self, request):
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if username == 'manager' and password == 'manager':
                auth.login(request, user)
                return redirect('cars/carshop_owner/owner_index')
            elif user is not None:
                auth.login(request, user)
                return redirect("cars/customer/customer_index")
            else:
                messages.info(request,'Invalid Credentials......')
                return redirect("cars/registration/login")
        
# The logout class
class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/')

# This class will show the car details in customer index page
class Customer_index(ListView):
    context_object_name  = 'cars'
    queryset = Cars.objects.all()
    template_name  = "cars/customer/customer_index.html"
    

# This class will show the car details in admin index page
class Owner_index(ListView):
    context_object_name  = 'cars'
    queryset = Cars.objects.all()
    template_name = "cars/carshop_owner/owner_index.html"

# This class will add the car details
class Add_car(View):
    form_class = CarsForm
    def get(self, request):
        carform = self.form_class()
        return render(request, "cars/carshop_owner/add_car.html", {'form': carform})
    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('cars/carshop_owner/owner_index')
            else:
                return redirect('cars/carshop_owner/add_car')
      

# This class will delete the car details
class Delete_car(View):
    def get(self, request, id):
        cars = Cars.objects.get(id=id)
        cars.delete()
        return redirect("cars/carshop_owner/owner_index")


# This class will edit/update the car details
class Edit_car(View):
    def get(self, request, id):
        cars = Cars.objects.get(id=id) 
        form = CarsForm(instance=cars)
        return render(request, 'cars/carshop_owner/edit_car.html', {'form':form})
    def post(self, request, id):
        if request.method == 'POST':
            cars = Cars.objects.get(id=id)
            form = CarsForm(request.POST,request.FILES, instance=cars)
            print(form)
            if form.is_valid():
                form.save()
                return redirect("cars/carshop_owner/owner_index")

# This class will display the car booked message
class Book_car(TemplateView):
    template_name = "cars/customer/book_car.html"


class CarDetailView(DetailView):
    model = Cars
    template_name = "cars/customer/car_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context  

@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
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
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )
    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id}) 


class PaymentFailedView(TemplateView):
    template_name = "cancel.html"

class PaymentSuccessView(TemplateView):
    template_name = "success.html"     

