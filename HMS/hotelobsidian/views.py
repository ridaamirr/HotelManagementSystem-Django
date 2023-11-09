from .models import *
from django.shortcuts import render, redirect 
from django.db import connection

def generate_bill(request):
    return render(request, 'generatebill.html')


def default(request): 
    #populating drop downs
    room_types = Roomtype.objects.values_list('type', flat=True).distinct()
    loc = Hotel.objects.values_list('location', flat=True).distinct()
    
    # If you want to execute the stored procedure, you can do it here
    cursor = connection.cursor()
    cursor.execute('call AutomaticCheckOut()') 
    logintype = request.session.get('logintype', None)
    context = {
        'loc':loc,
        'room_types': room_types, 
        'logintype':logintype,
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


def catalogue(request):  
    loc = Hotel.objects.values_list('location', flat=True).distinct()      
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype, 
       'loc':loc,
        }
    return render(request, 'catalogue.html',context) 

def cataloguelist(request):
    cursor = connection.cursor() 
    data=(request.GET.get('Location'),) 
    location=request.GET.get('Location') 
    print(location)
    cursor.callproc('catalog',data)
    result = cursor.fetchall()
    logintype = request.session.get('logintype', None)
    context = {
        'result':result,
        'logintype':logintype, 
        'location':location
         }   
    return render(request, 'catalogue.html', context)

#temp global variables cuz i was unable to pass values in function :')
globalroomid=1 
locat="abc" 
def booking(request,loc,roomid):  
    global locat  # Declare that locat refers to the global variable
    logintype = request.session.get('logintype', None)   
    print(loc) 
    locat=loc
    global globalroomid 
    globalroomid=roomid 
    context = {
        'logintype':logintype, 
        'roomid':roomid, 
        }  
    return render(request, 'catalogue.html', context)

def booking_final(request):
    username = request.session.get('username', None) 
    logintype = request.session.get('logintype', None) 
    days = request.GET.get('nodays')
    cursor = connection.cursor()   
    data = (username,globalroomid, locat,days) 
    print(data)
    cursor.callproc('BookRoom', data)
    context = {
        'logintype':logintype
        }  
    return redirect('catalogue')
    

def login(request):
    return render(request, 'login.html')

def admin(request): 
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype,
        }
    return render(request, 'admin.html',context)

def branchinformation(request): 
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype,
        }
    return render(request, 'branchinformation.html',context)

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
