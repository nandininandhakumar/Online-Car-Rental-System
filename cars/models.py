# from distutils.command.upload import upload
# from email.mime import image
# from unicodedata import name
from django.db import models


from django.contrib.auth.models import User

# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver

# Model to support Subscriptions

class CustomerStatus(models.Model):
    STATUSES = [
        ('active', 'active'),
        ('pause', 'pause'),
        ]

    status = models.CharField(max_length=15, choices=STATUSES, unique=True)

    def __str__(self):
        return self.status

class Customer(models.Model): 
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,related_name="customer")
    #stripeid means customerid when creates subscription
    stripeid = models.CharField(max_length=255,blank=True)
    stripe_subscription_id = models.CharField(max_length=255,blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)

    status = models.ForeignKey(CustomerStatus, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.user)

# post_save is used after saved in the database
@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        print(instance.username, "was just saved")

@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()
    
    





class Cars(models.Model):
    brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    price = models.IntegerField()
    picture = models.ImageField(upload_to = 'media',null=True,blank = True)

    def __str__(self):
        return self.car_model
