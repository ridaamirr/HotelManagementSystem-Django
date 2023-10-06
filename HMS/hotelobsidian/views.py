from .models import *
from django.shortcuts import render, redirect
from .forms import SignUpForm

# Create your views here

def default(request):
    return render(request, 'default.html') 

def login(request):
    return render(request, 'login.html')

def signup(request): 
    form = SignUpForm 
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login.html')  
        else: 
            return redirect('signup.html')
    context = {'form':form}
    return render(request, 'signup.html',context)