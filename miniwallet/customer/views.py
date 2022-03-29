from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

from customer.models import Customer

# Create your views here.
@csrf_exempt
def init_customer(request):
    if request.method == 'POST':
        new_id = request.POST['customer_xid']
        new_cust = Customer(id=new_id)
        try:
            new_cust = Customer.objects.get(pk = new_id)
            return JsonResponse({"error":"customer already exist"}, status=400)
        except:
            new_cust.token = get_random_string(length=32)
            response = {
                "data": {
                    "token": new_cust.token
                },
                "status": "success"
            }
            new_cust.save()
            return JsonResponse(response, status=200)