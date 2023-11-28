from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Hotel, Roomtype, Room
from django.urls import reverse
from django.contrib import messages

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
    print("Add damit")
    try:
        print("here")
        print("Request URL:", request.get_full_path())
        room_type = Roomtype.objects.get(roomtype_id=room_type_id)
        print(room_type)
        data = {
            'type': room_type.type,
            'noofbeds': room_type.numberofbeds,
            'price': room_type.price,
            'request_path': request.path,
        }
        return JsonResponse(data)
    except Roomtype.DoesNotExist:
        return JsonResponse({'error': f'Room Type with id {room_type_id} not found'}, status=400)

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
                isbooked='No',
            )

            messages.success(request, 'Room entry added successfully')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=400)


