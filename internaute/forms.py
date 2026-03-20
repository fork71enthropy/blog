from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Internaute


class InscriptionForm(UserCreationForm):
    class Meta:
        model = Internaute
        fields = ['username','first_name','last_name','email']
