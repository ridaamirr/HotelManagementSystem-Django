from .models import *
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Hotel
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)

def sample_view(request):
    print("This is a sample view statement.")
    return HttpResponse("Sample view executed successfully.")

def default(request): 
    #populating drop downs
    room_types = Roomtype.objects.values_list('type', flat=True).distinct()
    loc = Hotel.objects.values_list('location', flat=True).distinct()
    
    # If you want to execute the stored procedure, you can do it here
    cursor = connection.cursor()
    cursor.execute('call AutomaticCheckOut()')  
    logintype = request.session.get('logintype', None) 
    username = request.session.get('username', None) 
    cursor.execute("SELECT * FROM billing where User_ID=%s and Status='Not Paid'",[str(username)]) 
    results = cursor.fetchall()    
    context = {
        'loc':loc,
        'room_types': room_types, 
        'logintype':logintype, 
        'results':results,
        }     
    return render(request, 'default.html', context) 

from django.http import JsonResponse

def logout(request):
    request.session['logintype'] = None
    request.session['username'] = None 
    return redirect('login')


def checkavailabilty(request):
    if request.method == 'POST':
        location = request.POST.get('Location')
        room_type = request.POST.get('Type')
        no_of_beds = request.POST.get('noofbeds')

        cursor = connection.cursor()
        data = (location, room_type, no_of_beds)
        cursor.callproc('CheckAvailability', data)
        result = cursor.fetchall()
        temptohide = 1 
        return render(request, 'default.html', {'result': result, 'temptohide': temptohide,})
    else:
        return render(request, 'default.html')

    
def login(request):
    return render(request, 'login.html')

def admin(request): 
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype,
        }
    return render(request, 'admin/admin.html',context)


# Admin dashboard tiles--------------------------------------------------------------
def roominformation(request): 
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype,
        }
    return render(request, 'admin/roominformation.html',context)
def roomtype(request): 
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype,
        }
    return render(request, 'admin/roomtype.html',context)
def branchinformation(request): 
    logintype = request.session.get('logintype', None)   
    results = Hotel.objects.all()
    context = { 
        'results':results,
       'logintype':logintype,
        }
    return render(request, 'admin/branchinformation.html',context)
def customerinformation(request): 
    logintype = request.session.get('logintype', None)  
    results = Customer.objects.all()
    context = {
       'logintype':logintype, 
        'items':results,
        }
    return render(request, 'user/information.html',context)

def bookinginformation(request):   
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM CurrentBookings")
    data = cursor.fetchall() 
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype, 
       'items':data
        }
    return render(request, 'bookinginformation.html',context)


def payments(request):  
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM Billing")
    results = cursor.fetchall()  
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype, 
        'results':results,
        }
    return render(request, 'admin/payments.html',context)
#------------------------------------------------------------------------------------

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