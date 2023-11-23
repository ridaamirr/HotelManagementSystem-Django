import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import logging 

def payments_search(request):  
    search_type = request.POST.get('searchtype')
    search_value = request.POST.get('SearchBox') 
    cursor = connection.cursor()  
    print(search_type) 
    print(search_value)
    if search_value:
        if search_type == 'cnicradio':
            cursor.execute("SELECT * FROM billing where User_ID=%s",[str(search_value)])
        elif search_type == 'idradio':
            cursor.execute("SELECT * FROM billing where Billing_ID=%s",[str(search_value)])
        else:
            results = None
    else: 
        cursor.execute("SELECT * FROM billing")
    results = cursor.fetchall()   
    print(results) 
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype, 
       'results':results
        }
    return render(request, 'admin/payments.html',context) 

def paid(request,id): 
    cursor = connection.cursor()   
    data = (id)
    cursor.callproc('Paid', data)
    return redirect('payments') 

def billdetails(request): 
    logintype = request.session.get('logintype', None) 
    context = { 
        
       'logintype':logintype, 
        }
    return render(request, 'admin/billdetails.html',context) 