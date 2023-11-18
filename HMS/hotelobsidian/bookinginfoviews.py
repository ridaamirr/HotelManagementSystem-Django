import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import logging 

def checkout_Room_byadmin(request,roomid):
    cursor = connection.cursor()   
    username = request.session.get('username', None) 
    data=(roomid,username,)  
    cursor.callproc('checkoutRoom',data)
    return redirect('bookinginformation')  

def bookings_search(request):  
    search_type = request.POST.get('searchtype')
    search_value = request.POST.get('SearchBox') 
    cursor = connection.cursor() 
    if search_value:
        if search_type == 'cnicradio':
            cursor.execute("SELECT * FROM CurrentBookings where CNIC=%s",[str(search_value)])
        elif search_type == 'locradio':
            cursor.execute("SELECT * FROM CurrentBookings where Location=%s",[str(search_value)])
        elif search_type == 'roomoradio': 
            cursor.execute("SELECT * FROM CurrentBookings where RoomNumber=%s",[str(search_value)])
        else:
            results = None
    else: 
        cursor.execute("SELECT * FROM CurrentBookings")
    data = cursor.fetchall()   
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype, 
       'items':data
        }
    return render(request, 'bookinginformation.html',context)
