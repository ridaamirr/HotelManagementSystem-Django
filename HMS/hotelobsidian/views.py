from django.shortcuts import render, redirect
from .models import Customer
from django.contrib import messages

# Create your views here

def default(request):
    return render(request, 'default.html') 

def login(request):
    return render(request, 'login.html')

def user_dashboard(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    #print("Username:", username)
    #print("Password:", password)
    #sys.exit()
    try:
        user_data_row = Customer.objects.get(pk = username,password = password)
    except Customer.DoesNotExist:
        messages.error(request, "Invalid information entered")
        return redirect(request.META.get('HTTP_REFERER', 'default'))
    return render(request, 'user/dashboard.html')