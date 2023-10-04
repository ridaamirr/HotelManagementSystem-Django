from django.shortcuts import render, redirect
from .models import Customer, AdminLogin
from django.contrib import messages
from .forms import LoginForm

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
            return render(request, 'default.html')
        else:
            messages.error(request, "Invalid information entered")
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})