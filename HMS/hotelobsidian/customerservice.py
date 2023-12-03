from .models import Customer

class CustomerService:
    @staticmethod
    def search_customers(search_value):
        if search_value:
            results = Customer.objects.filter(cnic=search_value)
        else:
            results = Customer.objects.all()
        return results