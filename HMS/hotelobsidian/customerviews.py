from django.shortcuts import render
from django.db import connection
from .customerservice import CustomerService

def customer_search(request):
    search_value = request.POST.get('SearchBox')
    
    results = CustomerService.search_customers(search_value)
    
    logintype = request.session.get('logintype', None)
    context = {
        'logintype': logintype,
        'items': results,
    }
    
    return render(request, 'user/information.html', context)
