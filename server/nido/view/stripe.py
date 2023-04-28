from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import stripe
from django.conf import settings
from nido.models import DonationOption
from django.core import serializers


import json

stripe.api_key = settings.STRIPE_HOOKS_SECRET


def checkout(request):
    options = DonationOption.objects.all()
    return render(request, 'stripe/checkout.html', {'options': options})
 
@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        
        try:
            # customer = stripe.Customer.create()
            data = json.loads(request.body)
            # data = json.loads(request.POST)
            print(data)

            def calculate_order_amount(items):
                print(items)
                # total_amount=0
                # test_amount = items.amount
                # for item in items:
                #     total_amount += item.amount # replace "price" with the attribute name that holds the price of the item
                return 5000


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
