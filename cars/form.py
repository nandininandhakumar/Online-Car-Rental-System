from pyexpat import model
from django import forms
from cars.models import Cars

class CarsForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = "__all__"

