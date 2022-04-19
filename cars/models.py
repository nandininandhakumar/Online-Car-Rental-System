from distutils.command.upload import upload
from email.mime import image
from unicodedata import name
from django.db import models

# Create your models here.

class Cars(models.Model):
    brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    price = models.IntegerField()
    picture = models.ImageField(upload_to = 'media',null=True,blank = True)

    def __str__(self):
        return self.car_model
