from django.shortcuts import get_object_or_404
from .models import Hotel

class HotelService:
    @staticmethod
    def add_hotel(location, phone_number):
        if not location or not phone_number:
            raise ValueError('Location and Phone Number are required.')

        new_hotel = Hotel(location=location, phonenumber=phone_number)
        new_hotel.save()
        return new_hotel

    @staticmethod
    def update_hotel(branch_id, new_phonenumber):
        hotel = get_object_or_404(Hotel, pk=branch_id)
        before_update_message = f'Before Update - Branch ID: {branch_id}, Phone Number: {hotel.phonenumber} new number: {new_phonenumber}'

        hotel.phonenumber = new_phonenumber
        hotel.save()

        updated_hotel = get_object_or_404(Hotel, pk=branch_id)
        after_update_message = f'After Update - Branch ID: {branch_id}, Phone Number: {updated_hotel.phonenumber}'

        return before_update_message, after_update_message

    @staticmethod
    def delete_hotel(branch_id):
        branch = get_object_or_404(Hotel, pk=branch_id)
        branch.delete()
        return f"Deleted branch with ID {branch_id}"

    @staticmethod
    def get_hotels_by_criteria(search_type, search_value):
        if search_value:
            if search_type == 'idradio':
                try:
                    search_value = int(search_value)
                    results = Hotel.objects.filter(branch_id=search_value)
                except ValueError:
                    results = None
            elif search_type == 'locradio':
                results = Hotel.objects.filter(location=search_value)
            elif search_type == 'phoneradio':
                results = Hotel.objects.filter(phonenumber=search_value)
            else:
                results = None
        else:
            results = Hotel.objects.all()

        return results