from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Roomtype
from .roomtypeservice import RoomtypeService

class RoomtypeAddView(View):
    template_name = 'debug/error.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        number_of_beds = request.POST.get('BedNo')
        price = request.POST.get('Price')
        room_type = request.POST.get('DropDownList2')
        image = request.FILES.get('Image')

        try:
            new_roomtype = RoomtypeService.add_roomtype(number_of_beds, price, room_type, image)
            messages.success(request, 'Room type added successfully!')
            return redirect(request.META['HTTP_REFERER'])
        except ValueError as e:
            return render(request, self.template_name, {'error_message': str(e)})

    def get(self, request):
        return render(request, self.template_name)


class RoomtypeUpdateView(View):
    template_name = 'admin/roomtype.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        search_type = request.POST.get('searchtype')
        search_value = request.POST.get('SearchRoom')

        results = RoomtypeService.get_roomtypes_by_criteria(search_type, search_value)

        return render(request, self.template_name, {'results': results})

    def get(self, request):
        return HttpResponse("Invalid request method")


class DeleteRoomtypeView(View):
    def delete(self, request, roomtype_id):
        message = RoomtypeService.delete_roomtype(roomtype_id)
        return JsonResponse({'message': message})

class UpdateRoomtypeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, roomtype_id):
        data = json.loads(request.body.decode('utf-8'))
        try:
            before_update_message, after_update_message = RoomtypeService.update_roomtype(roomtype_id, data.get('new_no_of_beds'), data.get('new_price'))
            print(before_update_message)
            print(after_update_message)
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
        except Roomtype.DoesNotExist:
            messages.error(request, f"Room type with ID {roomtype_id} does not exist.")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)