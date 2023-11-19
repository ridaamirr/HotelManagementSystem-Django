import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import logging 

def checkout_byadmin(request,roomid):
    cursor = connection.cursor()   
    username = request.session.get('username', None) 
    data=(roomid,username,)  
    cursor.callproc('Checkout',data)
    return redirect('payments')  

def payments_search(request):  
    search_type = request.POST.get('searchtype')
    search_value = request.POST.get('SearchBox') 
    cursor = connection.cursor() 
    if search_value:
        if search_type == 'cnicradio':
            cursor.execute("SELECT * FROM billing where User_ID=%s",[str(search_value)])
        elif search_type == 'idradio':
            cursor.execute("SELECT * FROM billing where Billing_ID=%s",[str(search_value)])
        else:
            results = None
    else: 
        cursor.execute("SELECT * FROM billing")
    data = cursor.fetchall()   
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype, 
       'items':data
        }
    return render(request, 'payments.html',context)
