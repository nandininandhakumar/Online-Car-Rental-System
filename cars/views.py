from re import template
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from cars.form import CarsForm
from cars.models import Cars
from django.views import View

from django.views.generic import TemplateView
# Create your views here.

#The index page
# def index(request):
#     return render(request,'cars/index.html')

class Index(TemplateView):
    template_name = 'cars/index.html'

# This function will register the customer
# def registration(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         password2 = request.POST['password2']

#         if password == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'Username is already exist')
#                 return redirect('cars/registration/registration')
#             else:
#                 user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
#                 user.save()
#                 messages.info(request, 'customer registered')
#                 return redirect("cars/registration/login")
#         else:
#             messages.info(request,'password is not matching')
#             return redirect('cars/registration/registration')
#     else:
#         return render(request,'cars/registration/registration.html')


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





# This function is login for admin and customer
def login(request):
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
    else:
        return render(request,'cars/registration/login.html')




# The logout function
def logout(request):
    auth.logout(request)
    return redirect('/')

# This function will show the car details in customer index page
def customer_index(request):
    cars = Cars.objects.all()
    return render(request,'cars/customer/customer_index.html',{'cars':cars})

# This function will show the car details in admin index page
def owner_index(request):
    cars = Cars.objects.all()
    return render(request,'cars/carshop_owner/owner_index.html',{'cars':cars})

# This function will add the car details
def add_car(request):
    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cars/carshop_owner/owner_index')
        else:
            print('.................................................')
            return redirect('cars/carshop_owner/add_car')
    else:
        carform = CarsForm()
        return render(request, "cars/carshop_owner/add_car.html", {'form': carform})

# This function will delete the car details
def delete_car(request, id):
    cars = Cars.objects.get(id=id)
    cars.delete()
    return redirect("cars/carshop_owner/owner_index")

# This function will edit/update the car details
def edit_car(request, id):
    if request.method == 'POST':
        cars = Cars.objects.get(id=id)
        form = CarsForm(request.POST,request.FILES, instance=cars)
        print(form)
        
        if form.is_valid():
            form.save()
            return redirect("cars/carshop_owner/owner_index")
    else:
        cars = Cars.objects.get(id=id) 
        form = CarsForm(instance=cars)
    return render(request, 'cars/carshop_owner/edit_car.html',{'form':form})


# This function will display the car booked message
def book_car(request):
    return render(request,'cars/customer/book_car.html')
        

