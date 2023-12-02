from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Hotel, Roomtype, Room
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
import json

def roominformation_add(request):
    unique_locations = Hotel.objects.values('location').distinct()
    locations = [location['location'] for location in unique_locations]
    room_type_ids = Roomtype.objects.values_list('roomtype_id', flat=True)

    response_data = {
        'locations': locations,
        'room_type_ids': list(room_type_ids),
    }

    return JsonResponse(response_data, safe=False)

def roominformation_add_new(request, room_type_id):
    try:
        room_type = Roomtype.objects.get(roomtype_id=room_type_id)

        base_url = reverse('add_new_roominformation_form', kwargs={'room_type_id': 0})
        url_without_info = base_url.replace('0/', '')
        redirect_url = reverse('roominformation_add')
        data = {
            'type': room_type.type,
            'noofbeds': room_type.numberofbeds,
            'price': room_type.price,
            'request_path': redirect_url,
        }
        print("Final Data:", data)

        return JsonResponse(data)
    except Roomtype.DoesNotExist:
        return JsonResponse({'error': f'Room Type with id {room_type_id} not found'}, status=400)

def roominformation_enter_data(request):
    if request.method == 'GET':
        try:
            room_type_id = int(request.GET.get('room_type_id'))
            room_number = int(request.GET.get('room_number'))

            existing_entry = Room.objects.filter(roomtype_id=room_type_id, roomnumber=room_number).exists()
            if existing_entry:
                messages.error(request, 'Entry with the same room number and type already exists')
                return JsonResponse({'error': 'Entry with the same room number and type already exists'}, status=400)

            location = request.GET.get('location')
            hotel = get_object_or_404(Hotel.objects.filter(location=location)[:1])

            room = Room.objects.create(
                roomtype_id=room_type_id,
                roomnumber=room_number,
                branch=hotel,
                isbooked='False',
            )

            messages.success(request, 'Room entry added successfully')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=400)

def roominformation_update(request):
    if request.method == 'POST':
        search_type = request.POST.get('searchtype')
        search_value = request.POST.get('SearchRoom')

        if search_value:
            if search_type == 'ID_Radio':
                try:
                    search_value = int(search_value)
                    results = Room.objects.filter(room_id=search_value)
                except ValueError:
                    results = None
            elif search_type == 'room_radio':
                try:
                    search_value = int(search_value)
                    results = Room.objects.filter(roomnumber=search_value)
                except ValueError:
                    results = None
            elif search_type == 'type_radio':
                roomtype_ids = Roomtype.objects.filter(type=search_value).values_list('roomtype_id', flat=True)
                results = Room.objects.filter(roomtype__in=roomtype_ids)
            elif search_type == 'branch_radio':
                branch_ids = list(Hotel.objects.filter(location=search_value).values_list('branch_id', flat=True))
                results = Room.objects.filter(branch__in=branch_ids)
        else:
            results = Room.objects.all()

        table_data = []
        for room in results:
            row_data = [
                room.room_id,
                room.roomnumber,
                room.roomtype.type,
                room.roomtype.numberofbeds,
                room.branch.location,
            ]
            table_data.append(row_data)
        logintype = request.session.get('logintype', None)  
        
        return render(request, 'admin/roominformation.html', {'table_data': table_data,'logintype':logintype,})

    return HttpResponse("Invalid request method")

def delete_roominformation(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    room.delete()
    messages.success(request, f"Deleted room with ID {room_id}")
    return redirect(request.META.get('HTTP_REFERER', 'default_url'))

def update_roominformation(request, room_id):
    print("update_room function is being executed...")

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        new_room_number = data.get('new_room_number')
        print("new room number:", new_room_number)

        try:
            room = get_object_or_404(Room, pk=room_id)
            before_update_message = f'Before Update - Room ID: {room_id}, Room No: {room.roomnumber}'
            print(before_update_message)

            room.roomnumber = new_room_number
            room.save()

            updated_room = get_object_or_404(Room, pk=room_id)
            after_update_message = f'After Update - Room ID: {room_id}, Room No: {updated_room.roomnumber}'
            print(after_update_message)

            #messages.success(request, f"{before_update_message}. {after_update_message}")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
        except Room.DoesNotExist:
            messages.error(request, f"Room with ID {room_id} does not exist.")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)