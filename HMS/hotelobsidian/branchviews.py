from .models import *
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Hotel
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
#import logging

#logger = logging.getLogger(__name__)

#Branch Information CRUD-------------------------------------------------------------
def branchinformation_add(request):
    if request.method == 'POST':
        location = request.POST.get('Location')
        phone_number = request.POST.get('Phone')

        if not location or not phone_number:
            return render(request, 'debug/error.html', {'error_message': 'Location and Phone Number are required.'})

        new_hotel = Hotel(location=location, phonenumber=phone_number)
        new_hotel.save()

        messages.success(request, 'Hotel information added successfully!')
        return redirect(request.META['HTTP_REFERER'])

    return render(request, 'debug/error.html')

def branchinformation_update(request):
    if request.method == 'POST':
        search_type = request.POST.get('searchtype')
        search_value = request.POST.get('SearchBox')

        if search_value:
            if search_type == 'idradio':
                results = Hotel.objects.filter(branch_id=search_value)
            elif search_type == 'locradio':
                results = Hotel.objects.filter(location=search_value)
            elif search_type == 'phoneradio':
                results = Hotel.objects.filter(phonenumber=search_value)
            else:
                results = None
        else:
            # If the search box is empty, return the entire table
            results = Hotel.objects.all()

        return render(request, 'admin/branchinformation.html', {'results': results})

    return HttpResponse("Invalid request method")

def delete_branch(request, branch_id):
    branch = get_object_or_404(Hotel, pk=branch_id)
    branch.delete()
    messages.success(request, f"Deleted branch with ID {branch_id}")
    return redirect(request.META.get('HTTP_REFERER', 'default_url'))

def update_branch(request, branch_id):
    print("update_branch function is being executed...")

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        new_phonenumber = data.get('new_phonenumber')

        try:
            hotel = get_object_or_404(Hotel, pk=branch_id)
            before_update_message = f'Before Update - Branch ID: {branch_id}, Phone Number: {hotel.phonenumber} new number: {new_phonenumber}'
            print(before_update_message)

            hotel.phonenumber = new_phonenumber
            hotel.save()

            updated_hotel = get_object_or_404(Hotel, pk=branch_id)
            after_update_message = f'After Update - Branch ID: {branch_id}, Phone Number: {updated_hotel.phonenumber}'
            print(after_update_message)

            #messages.success(request, f"{before_update_message}. {after_update_message}")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
        except Hotel.DoesNotExist:
            messages.error(request, f"Branch with ID {branch_id} does not exist.")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

#------------------------------------------------------------------------------------