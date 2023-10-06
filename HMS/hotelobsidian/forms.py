from django import forms 
from .models import Customer

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    adminusername = forms.CharField(label="Adminusername")
    password = forms.CharField(label="Password", widget=forms.PasswordInput()) 

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):  
      cnic= forms.CharField(label="CNIC", max_length=20) 
      firstname=forms.CharField(label="FirstName") 
      lastname=forms.CharField(label="LastName")
      email = forms.CharField(label="Email")
      phonenumber = forms.CharField(label='PhoneNumber',max_length = 20)
      address=forms.CharField(label="Address") 
      password=forms.CharField(label="Password") 
      dob=forms.CharField(label="DOB")
      class Meta: 
             model = Customer
             fields = ['cnic', 'firstname', 'lastname', 'phonenumber', 'email','address','dob','password']
       

        