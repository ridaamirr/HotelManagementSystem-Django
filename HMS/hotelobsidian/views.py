from django.shortcuts import render

# Create your views here

def default(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'default.html') 

def login(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'login.html')
