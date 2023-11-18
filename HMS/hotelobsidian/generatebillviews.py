import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Room, Roomtype
from django.contrib import messages
from django.http import HttpResponse
import logging

#Generate Bill Views-----------------------------------------------------------------------
def generate_bill(request): 
    #print total bill as well
    cursor = connection.cursor()   
    username = request.session.get('username', None) 
    data=(username,)  
    cursor.execute('call TotalBill()')
    result=cursor.fetchall()
    print(result)
    cursor.callproc('BookedRoom',data)
    result = cursor.fetchall() 
    logintype = request.session.get('logintype', None)
    context = {
        'items':result,
        'logintype':logintype, 
        }   
    return render(request, 'generatebill.html',context)

def checkout_Room(request,roomid):
    cursor = connection.cursor()   
    username = request.session.get('username', None) 
    data=(roomid,username,)  
    cursor.callproc('checkoutRoom',data)
    return redirect('generate_bill') 

def checkoutAll(request): 
    cursor = connection.cursor()   
    username = request.session.get('username', None) 
    data=(username,)  
    cursor.callproc('CheckOut',data)
    return redirect('generate_bill') 
#----------------------------------------------------------------------------------------------------