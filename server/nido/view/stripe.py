from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import stripe
from django.conf import settings
from nido.models import DonationOption
from django.core import serializers
import json


import json

stripe.api_key = settings.STRIPE_HOOKS_SECRET


def checkout(request):
    options = DonationOption.objects.all().order_by('-id')
    return render(request, 'stripe/checkout.html', {'options': options})
 
def calculate_order_amount(items):
    print("the items are:")
    print(items)    

    if items == [{'id': '1'}] :
        return 500000
    elif items == [{'id': '2'}] :
        return 100000
    elif items == [{'id': '3'}] :
        return 35000
    else:
        return 5000
    
@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        
        try:
            # customer = stripe.Customer.create()
            data = json.loads(request.body)
            # data = json.loads(request.POST)
            # print(data)



            intent = stripe.PaymentIntent.create(
                amount=calculate_order_amount(data['items']),
                currency='mxn',
                # automatic_payment_methods={
                #     'enabled': True,
                # },
                payment_method_types=['card', 'oxxo'],
                # The parameter is optional. The default value of expires_after_days is 3.
                payment_method_options={
                    'oxxo' : {
                        'expires_after_days': 2
                    }
                },
            )
            clientSecret = intent['client_secret']
            # print(intent)
            return HttpResponse(
                json.dumps({'clientSecret': clientSecret}),
                content_type='application/json')

        except Exception as e:

            return HttpResponse(
                json.dumps({'error :c': str(e)}),
                content_type='application/json'
            )

    # POST only View, Raise Error
    from django.http import Http404
    print("ndkjfndskj")
    raise Http404
