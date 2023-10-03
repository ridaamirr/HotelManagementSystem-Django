from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages

# Create your views here

def default(request):
    return render(request, 'default.html') 

def login(request):
    return render(request, 'login.html')