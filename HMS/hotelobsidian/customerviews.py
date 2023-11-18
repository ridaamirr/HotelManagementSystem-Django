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

def customer_search(request): 
    search_value = request.POST.get('SearchBox')  
    cursor = connection.cursor() 
    if search_value:
       results = Customer.objects.filter(cnic=search_value)
    else: 
        results = Customer.objects.all()
    logintype = request.session.get('logintype', None) 
    context = {
       'logintype':logintype, 
        'items':results,
        }
    return render(request, 'user/information.html',context)