from django.shortcuts import render

# Create your views here

def default(request):
    return render(request, 'default.html') 

def login(request):
    return render(request, 'login.html')