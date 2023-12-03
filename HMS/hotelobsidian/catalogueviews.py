import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Hotel
from django.contrib import messages
from django.http import HttpResponse 

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
    return redirect('catalogue')