from django.http import HttpResponseForbidden, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from customer.models import Customer

from wallet.models import Deposits, Wallet, Withdrawals
from wallet.serializer import DepositsSerializer, WalletSerializer, WithdrawalSerializer

# Create your views here.
@csrf_exempt
def wallet_list(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            wallets = Wallet.objects.all()
            serializer = WalletSerializer(wallets, many=True)
            return JsonResponse(serializer.data, safe=False)
        new_auth = request.META['HTTP_AUTHORIZATION']
        new_auth = new_auth.split(" ")[1]
        cust = Customer.objects.filter(token=new_auth).first()
        wallet = Wallet.objects.filter(owned_by = cust.id).first()
        if wallet:
            if wallet.status == 'enabled':
                serializer = WalletSerializer(wallet)
                response = {'status': 'success'}
                response['data'] = {'wallet': serializer.data}
                return JsonResponse(response)   
        return HttpResponseForbidden("please enable your wallet first")

    elif request.method == 'POST':
        new_auth = request.META['HTTP_AUTHORIZATION']
        new_auth = new_auth.split(" ")[1]
        cust = Customer.objects.filter(token=new_auth).first()
        wallet = Wallet.objects.filter(owned_by = cust.id).first()
        if wallet:
            if wallet.status == 'enabled':
                return HttpResponseForbidden("cannot enable already enabled wallet")
        wallet = Wallet(owned_by=cust)
        wallet.save()
        serializer = WalletSerializer(wallet)
        response = {'status': 'success'}
        response['data'] = {'wallet': serializer.data}
        return JsonResponse(response)

    elif request.method == 'PATCH':
        new_auth = request.META['HTTP_AUTHORIZATION']
        new_auth = new_auth.split(" ")[1]
        patch = QueryDict(request.body)
        is_disabled = patch.get('is_disabled')
        cust = Customer.objects.filter(token=new_auth).first()
        wallet = Wallet.objects.filter(owned_by = cust.id).first()
        if wallet:
            if is_disabled == 'true':
                if wallet.status == 'disabled':
                    return HttpResponseForbidden("cannot disable already disabled wallet")
                wallet.status = 'disabled'
                wallet.save()
                serializer = WalletSerializer(wallet)
                response = {'status': 'success'}
                response['data'] = {'wallet': serializer.data}
                return JsonResponse(response)
        return HttpResponseForbidden("no wallet exist")

    

@csrf_exempt
def withdrawl(request):
    if request.method == 'POST':
        new_auth = request.META['HTTP_AUTHORIZATION']
        new_auth = new_auth.split(" ")[1]
        amount = request.POST['amount']
        if 'refernce_id' in request.POST:
            reference_id = request.POST['reference_id']
        cust = Customer.objects.filter(token=new_auth).first()
        wallet = Wallet.objects.filter(owned_by = cust.id).first()
        if wallet:
            if wallet.status == 'enabled':
                try:
                    wallet.balance -= int(amount)
                    wallet.save()
                    withdraw = Withdrawals(amount=amount)
                    withdraw.owned_by = wallet
                    withdraw.withdrawn_by = cust
                    if reference_id:
                        withdraw.reference_id = reference_id
                    withdraw.save()
                    serializer = WithdrawalSerializer(withdraw)
                    response = {'status': 'success'}
                    response['data'] = {'wallet': serializer.data}
                    return JsonResponse(response)  
                except:
                    return HttpResponseForbidden("not enough balance or reference_id is wrong")
        return HttpResponseForbidden("please enable your wallet first")@csrf_exempt

@csrf_exempt
def deposit(request):
    if request.method == 'POST':
        new_auth = request.META['HTTP_AUTHORIZATION']
        new_auth = new_auth.split(" ")[1]
        amount = request.POST['amount']
        reference_id = None
        if 'refernce_id' in request.POST:
            reference_id = request.POST['reference_id']
        cust = Customer.objects.filter(token=new_auth).first()
        wallet = Wallet.objects.filter(owned_by = cust.id).first()
        if wallet:
            if wallet.status == 'enabled':
                try:
                    wallet.balance += int(amount)
                    wallet.save()
                    deposit = Deposits(amount=amount)
                    deposit.owned_by = wallet
                    deposit.deposited_by = cust
                    if reference_id:
                        deposit.reference_id = reference_id
                    deposit.save()
                    serializer = DepositsSerializer(deposit)
                    response = {'status': 'success'}
                    response['data'] = {'wallet': serializer.data}
                    return JsonResponse(response)
                except:
                    return HttpResponseForbidden("something wrong with reference_id or balance")
        return HttpResponseForbidden("please enable your wallet first")
