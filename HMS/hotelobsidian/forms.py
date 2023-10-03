from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    adminusername = forms.CharField(label="Adminusername")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

