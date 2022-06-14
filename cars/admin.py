from django.contrib import admin
from .models import Cars, Customer, CustomerStatus

# Register your models here.


admin.site.register(Cars)
admin.site.register(Customer)
admin.site.register(CustomerStatus)
