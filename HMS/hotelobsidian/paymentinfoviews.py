from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.http import HttpResponse

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
    results = cursor.fetchall()   
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

def billdetails(request,id): 
    logintype = request.session.get('logintype', None)  
    cursor=connection.cursor()
    data = (id)
    cursor.callproc('ViewBooking', data)    
    result = cursor.fetchall()  
    cursor.execute('SELECT TotalBillById(%s) AS TotalBill;',id)
    totalbill=cursor.fetchall()[0][0]  
    cursor.execute('SELECT isBillPresent(%s) AS Bill;',id)
    billpresence=cursor.fetchall()[0][0]  
    context = { 
        'items1':result, 
        'totalbill':totalbill,
       'logintype':logintype, 
       'bill':billpresence, 
        }
    return render(request, 'admin/billdetails.html',context) 