from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Hotel
from .hotelservices import HotelService

class BranchInformationAddView(View):
    template_name = 'debug/error.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        location = request.POST.get('Location')
        phone_number = request.POST.get('Phone')

        try:
            new_hotel = HotelService.add_hotel(location, phone_number)
            messages.success(request, 'Hotel information added successfully!')
            return redirect(request.META['HTTP_REFERER'])
        except ValueError as e:
            return render(request, self.template_name, {'error_message': str(e)})

    def get(self, request):
        return render(request, self.template_name)


class BranchInformationUpdateView(View):
    template_name = 'admin/branchinformation.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        search_type = request.POST.get('searchtype')
        search_value = request.POST.get('SearchBox')

        results = HotelService.get_hotels_by_criteria(search_type, search_value)

        return render(request, self.template_name, {'results': results})

    def get(self, request):
        return HttpResponse("Invalid request method")


class DeleteBranchView(View):
    def get(self, request, branch_id):
        message = HotelService.delete_hotel(branch_id)
        messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER', 'default_url'))


class UpdateBranchView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, branch_id):
        data = json.loads(request.body.decode('utf-8'))
        try:
            before_update_message, after_update_message = HotelService.update_hotel(branch_id, data.get('new_phonenumber'))
            print(before_update_message)
            print(after_update_message)
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
        except Hotel.DoesNotExist:
            messages.error(request, f"Branch with ID {branch_id} does not exist.")
            return redirect(request.META.get('HTTP_REFERER', 'default_url'))
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)