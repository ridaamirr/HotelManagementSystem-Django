from .models import *
from django.shortcuts import render, redirect 
from django.db import connection 

# Create your views here

def default(request):  
    results=Hotel.objects.all()
    cursor=connection.cursor()
    cursor.execute('call AutomaticCheckOut()')  
    return render(request, 'default.html', {"results":results})

def login(request):
    return render(request, 'login.html')

def admin(request):
    return render(request, 'admin.html')

def signup(request): 
    if request.method == 'POST': 
        if request.POST.get('cnic') and request.POST.get('firstname') and request.POST.get('lastname') and request.POST.get('email') and request.POST.get('phonenumber') and request.POST.get('password') and request.POST.get('dob') and request.POST.get('address'):
            saverecord=Customer()
            saverecord.cnic=request.POST.get('cnic')
            saverecord.firstname=request.POST.get('firstname')
            saverecord.lastname=request.POST.get('lastname')
            saverecord.email=request.POST.get('email')
            saverecord.password=request.POST.get('password') 
            saverecord.dob=request.POST.get('dob')
            saverecord.address=request.POST.get('address')
            saverecord.phonenumber=request.POST.get('phonenumber') 
            saverecord.save()
            return render(request,'login.html')      
    return render(request,'signup.html')
