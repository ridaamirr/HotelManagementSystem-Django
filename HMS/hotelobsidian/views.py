from .models import *
from django.shortcuts import render, redirect 
from django.db import connection
from .models import Room

def default(request): 
    #populating drop downs
    room_types = Roomtype.objects.values_list('type', flat=True).distinct()
    loc = Hotel.objects.values_list('location', flat=True).distinct()
    
    # If you want to execute the stored procedure, you can do it here
    cursor = connection.cursor()
    cursor.execute('call AutomaticCheckOut()') 

    context = {
        'loc':loc,
        'room_types': room_types,
         }     
    return render(request, 'default.html', context) 

def checkavailabilty(request): 
    if request.method == 'POST': 
        cursor = connection.cursor()
        cursor.execute('call CheckAvailability(%s, %s, %s)',request.GET.get('Location'),request.GET.get('Type'),request.GET.get('noofbeds'))
        result=cursor.fetchone()

    if result is None:
         return(request,'signup.html') 
    else:
        return(request,'default.html',{ 'result':result} )  



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
