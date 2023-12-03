from django.shortcuts import get_object_or_404
from .models import Roomtype

class RoomtypeService:
    @staticmethod
    def add_roomtype(number_of_beds, price, room_type, image):
        if not number_of_beds or not price or not image or not room_type:
            raise ValueError('Number of beds, price, image, and room type are required.')

        new_roomtype = Roomtype(numberofbeds=number_of_beds, price=price, type=room_type, image=image)
        new_roomtype.save()
        return new_roomtype

    @staticmethod
    def update_roomtype(roomtype_id, new_no_of_beds, new_price):
        roomtype = get_object_or_404(Roomtype, pk=roomtype_id)
        before_update_message = f'Before Update - Room Type ID: {roomtype_id}, NumberofBeds: {roomtype.numberofbeds} price: {roomtype.price}'

        roomtype.numberofbeds = new_no_of_beds
        roomtype.price = new_price
        roomtype.save()

        updated_roomtype = get_object_or_404(Roomtype, pk=roomtype_id)
        after_update_message = f'After Update - Room Type ID: {roomtype_id}, NumberofBeds: {updated_roomtype.numberofbeds} price: {updated_roomtype.price}'

        return before_update_message, after_update_message

    @staticmethod
    def delete_roomtype(roomtype_id):
        roomtype = get_object_or_404(Roomtype, pk=roomtype_id)
        roomtype.delete()
        return f"Deleted room type with ID {roomtype_id}"

    @staticmethod
    def get_roomtypes_by_criteria(search_type, search_value):
        if search_value:
            if search_type == 'ID_radio':
                try:
                    search_value = int(search_value)
                    results = Roomtype.objects.filter(roomtype_id=search_value)
                except ValueError:
                    results = None
            elif search_type == 'Type_radio':
                results = Roomtype.objects.filter(type=search_value)
            elif search_type == 'No_of_beds_radio':
                try:
                    search_value = int(search_value)
                    results = Roomtype.objects.filter(numberofbeds=search_value)
                except ValueError:
                    results = None
            elif search_type == 'price_radio':
                try:
                    search_value = int(search_value)
                    results = Roomtype.objects.filter(price=search_value)
                except ValueError:
                    results = None
            else:
                results = None
        else:
            results = Roomtype.objects.all()

        return results