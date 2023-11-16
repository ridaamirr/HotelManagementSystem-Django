import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Room, Roomtype
from django.contrib import messages
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

#Room Type CRUD-------------------------------------------------------------
def roomtype_add(request):
    if request.method == 'POST':
        Type = request.POST.get('DropDownList2')
        Number_of_beds = request.POST.get('BedNo')
        Price = request.POST.get('Price')
        Image = request.FILES.get('Image')

        if not Number_of_beds or not Price or not Image or not Type:
            return render(request, 'debug/error.html', {'error_message': 'Bad Request.'})

        new_roomtype = Roomtype(numberofbeds=Number_of_beds, price=Price, type=Type, image=Image)
        new_roomtype.save()

        messages.success(request, 'Room type added successfully!')
        return redirect(request.META['HTTP_REFERER'])

    return render(request, 'debug/error.html')

def roomtype_update(request):
    if request.method == 'POST':
        search_type = request.POST.get('searchtype')
        search_value = request.POST.get('SearchRoom')

        if search_value:
            if search_type == 'ID_radio':
                results = Roomtype.objects.filter(roomtype_id=search_value)
            elif search_type == 'Type_radio':
                results = Roomtype.objects.filter(type=search_value)
            elif search_type == 'No_of_beds_radio':
                results = Roomtype.objects.filter(numberofbeds=search_value)
            elif search_type == 'price_radio':
                results = Roomtype.objects.filter(price=search_value)
            else:
                results = None
        else:
            results = Roomtype.objects.all()

        return render(request, 'admin/roomtype.html', {'results': results})

    return HttpResponse("Invalid request method")

def delete_room(request, room_id):
    branch = get_object_or_404(Hotel, pk=room_id)
    branch.delete()
    messages.success(request, f"Deleted branch with ID {room_id}")
    return redirect(request.META.get('HTTP_REFERER', 'default_url'))

def update_room(request, room_id):
    print("update_branch function is being executed...")

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        new_phonenumber = data.get('new_phonenumber')

        try:
            hotel = get_object_or_404(Hotel, pk=room_id)
            before_update_message = f'Before Update - Branch ID: {room_id}, Phone Number: {hotel.phonenumber} new number: {new_phonenumber}'
            print(before_update_message)

            hotel.phonenumber = new_phonenumber
            hotel.save()

            updated_hotel = get_object_or_404(Hotel, pk=room_id)
            after_update_message = f'After Update - Branch ID: {room_id}, Phone Number: {updated_hotel.phonenumber}'
            print(after_update_message)

            #messages.success(request, f"{before_update_message}. {after_update_message}")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
        except Hotel.DoesNotExist:
            messages.error(request, f"Branch with ID {room_id} does not exist.")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

#------------------------------------------------------------------------------------