
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from cars.form import CarsForm
from cars.models import Cars
from django.views import View

from django.views.generic import TemplateView, DeleteView, ListView, UpdateView
# Create your views here.


class Index(TemplateView):
    template_name = 'cars/index.html'

# This function will register the customer
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
        
# The logout function
class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/')

# This function will show the car details in customer index page
class Customer_index(ListView):
    context_object_name  = 'cars'
    queryset = Cars.objects.all()
    template_name  = "cars/customer/customer_index.html"
    

# This function will show the car details in admin index page
class Owner_index(ListView):
    context_object_name  = 'cars'
    queryset = Cars.objects.all()
    template_name = "cars/carshop_owner/owner_index.html"

# This function will add the car details
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
      

# This function will delete the car details
class Delete_car(View):
    def get(self, request, id):
        cars = Cars.objects.get(id=id)
        cars.delete()
        return redirect("cars/carshop_owner/owner_index")


# This function will edit/update the car details
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

# This function will display the car booked message
class Book_car(TemplateView):
    template_name = "cars/customer/book_car.html"
        

