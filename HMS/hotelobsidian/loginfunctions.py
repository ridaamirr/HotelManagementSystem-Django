from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Hotel,Customer,AdminLogin,Roomtype
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def user_dashboard(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        logintype = request.POST.get('logintype')
        if logintype == 'user':
            form.fields['username'].required = True
            form.fields['adminusername'].required = False
        elif logintype == 'admin':
            form.fields['adminusername'].required = True
            form.fields['username'].required = False
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            adminusername = form.cleaned_data['adminusername']
            request.session['logintype'] = logintype 
            request.session['username']=username
            try:
                if logintype=='user':
                    data_row = Customer.objects.get(pk=username, password=password)
                elif logintype=='admin':
                    data_row = AdminLogin.objects.get(pk=adminusername, password=password)
            except Customer.DoesNotExist:
                messages.error(request, "Invalid information entered")
                return redirect('login')
            except AdminLogin.DoesNotExist:
                messages.error(request, "Invalid information entered")
                return redirect('login')
            room_types = Roomtype.objects.values_list('type', flat=True).distinct()
            loc = Hotel.objects.values_list('location', flat=True).distinct()  
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM billing where User_ID=%s and Status='Not Paid'",[str(username)]) 
            results = cursor.fetchall()   
            return render(request, 'default.html',{'logintype':logintype,'loc':loc,'room_types': room_types, 'results':results,})
        else:
            messages.error(request, "Invalid information entered")
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})