from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
import stripe
from cars.form import CarsForm
from cars.models import Cars, Customer, CustomerStatus
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
    # queryset = Cars.objects.all()
    queryset = Cars.objects.get_queryset().order_by('id')
    template_name  = "cars/customer/customer_index.html"
    paginate_by = 1
    
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
        # context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['stripe_publishable_key'] = 'pk_test_51KpwlTSE5P0vwzLjK7Ri3NNG2IcW5X2s52wq5AQmyMaum82XqQ1hJZBDcTfT8kocxCrujKqn1UN3NBBsv3rCJZ7c00lLzozOEg'
        return context  

class PaymentFailedView(TemplateView):
    template_name = "cancel.html"

class PaymentSuccessView(TemplateView):
    template_name = "success.html"     

def home(request):
    return render(request, 'membership/home_sub.html')

# @login_required
def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'register/settings.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})

def join(request):
    return render(request, 'membership/join.html')

@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')

def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        print(session)
        customer = Customer.objects.get(user = request.user)
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription

        CustomerStatus.status = 'active'
        # customer.save()
        # print(customer)
        # customer = Customer.objects.create(user = request.user, stripeid =session.customer, membership = True, cancel_at_period_end = False, stripe_subscription_id = session.subscription )
        customer.save()
    # return render(request, 'membership/success_sub.html')
    
    return render(request, 'register/settings.html')


def cancel(request):
    return render(request, 'membership/cancel_sub.html')

# Permanantly delete Subscription 
def Deletesubscription(request):
    
    # Permanantly delete Subscription id from stripe account
    stripe.Subscription.delete(stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)),
    # Permanantly delete customername, stripeid(customerid according to subscription), status, membership from Customer model
    v=Customer.objects.get(user = request.user).delete()
    #creates user based on login
    customer = Customer.objects.create(user = request.user)
    return redirect('/deletemsg')

def Deletemsg(request):
    return render(request, "deletemsg.html")

def Pausepayment(request):
    stripe.Subscription.modify(
    request.user.customer.stripe_subscription_id,
    pause_collection={
        'behavior': 'mark_uncollectible',
    },
    )
    Customer.status = 'pause'
    return redirect('/pausemsg')

def Pausemsg(request):
    return render(request, "pausemsg.html")

def Resumepayment(request):
    stripe.Subscription.modify(
    request.user.customer.stripe_subscription_id,
    pause_collection='',
)
    Customer.status = 'active'
    return redirect('/resumemsg')


def Resumemsg(request):
    return render(request, "resumemsg.html")


# @login_required
def checkout(request):
    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 1000
        membership_id = 'price_1L0kZuSE5P0vwzLjTpdzEGoj'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1L0kZuSE5P0vwzLji6pj827J'
                final_dollar = 10000

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/success_sub?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel_sub',
        )

        return render(request, 'membership/checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})

def Upgrade(request):
 if request.method == 'GET' :
    subscription =  stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)

    stripe.Subscription.modify(
    subscription.id,
    cancel_at_period_end=False,
    proration_behavior='create_prorations',
    # proration_behavior='always_invoice',
    items=[{
        'id': subscription['items']['data'][0].id,
    
        'price': 'price_1L0kZuSE5P0vwzLji6pj827J',
    
    }]
    )
    return redirect('/upgrademsg')


def Upgrademsg(request):
    return render(request, "upgrademsg.html")


def Downgrade(request):
 if request.method == 'GET' :
    subscription =  stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)

    stripe.Subscription.modify(
    subscription.id,
    cancel_at_period_end=False,
    proration_behavior='create_prorations',
    # proration_behavior='always_invoice',
    items=[{
        'id': subscription['items']['data'][0].id,
    
        'price': 'price_1L0kZuSE5P0vwzLjTpdzEGoj',
    
    }]
    )
    return redirect('/downgrademsg')

def Downgrademsg(request):
    return render(request, "downgrademsg.html")







































































































































































































































































































