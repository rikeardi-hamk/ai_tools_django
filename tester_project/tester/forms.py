# tester/forms.py
from django import forms
from .models import Server

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'address']
