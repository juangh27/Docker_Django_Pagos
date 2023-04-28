# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
# from django.http import HttpResponse
# import stripe
# from django.conf import settings
# from nido.models import DonationOption
# from django.core import serializers


# import json

# stripe.api_key = settings.STRIPE_HOOKS_SECRET


# def checkout(request):
#     options = DonationOption.objects.all()
#     return render(request, 'stripe/checkout.html', {'options': options})
#     # return render(request, 'stripe/checkout.html', {'options_data': options_data})

# # The POST checkout form
# #
# # urlpattern: 
# #   path('create-payment-intent', views.create_payment, name='create_payment'),
# @csrf_exempt
# def create_payment(request):
#     if request.method == 'POST':
        
#         try:
#             # customer = stripe.Customer.create()
#             data = json.loads(request.body)
#             # data = json.loads(request.POST)
#             print(data)

#             def calculate_order_amount(items):
#                 print(items)
#                 # total_amount=0
#                 # test_amount = items.amount
#                 # for item in items:
#                 #     total_amount += item.amount # replace "price" with the attribute name that holds the price of the item
#                 return 5000

#             # this api_key could possibly go into settings.py like:
#             #   STRIPE_API_KEY = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
#             #
#             # and fetched out with:
#             #   from django.conf import settings
#             #   stripe.api_key = settings.STRIPE_API_KEY

#             # import stripe
#             # stripe.api_key = settings.STRIPE_HOOKS_SECRET

#             # raise Exception("I want to know the value of this: " + data)
#             # Create a PaymentIntent with the order amount and currency
#             intent = stripe.PaymentIntent.create(
#                 amount=calculate_order_amount(data['items']),
#                 currency='mxn',
#                 automatic_payment_methods={
#                     'enabled': True,
#                 },
#             )
#             clientSecret = intent['client_secret']
#             # print(intent)
#             return HttpResponse(
#                 json.dumps({'clientSecret': clientSecret}),
#                 content_type='application/json')
#             # return HttpResponse(
#             #     json.dumps({'clientSecret': intent['client_secret']}),
#             #     content_type='application/json'
#             # )
#         except Exception as e:

#             # Just return the 403 and NO error msg
#             #   Not sure how to raise a 403 AND return the error msg
#             # from django.http import HttpResponseForbidden
#             # return HttpResponseForbidden()

#             # OR you could return just the error msg
#             #   but the js would need to be changed to handle this
#             return HttpResponse(
#                 json.dumps({'error :c': str(e)}),
#                 content_type='application/json'
#             )

#     # POST only View, Raise Error
#     from django.http import Http404
#     print("ndkjfndskj")
#     raise Http404


# # from django.shortcuts import render
# # from django.views.decorators.http import require_POST
# # from django.http import JsonResponse, HttpRequest
# # import json


# # def calculate_order_amount(items):
# #     # Replace this constant with a calculation of the order's amount
# #     # Calculate the order total on the server to prevent
# #     # people from directly manipulating the amount on the client
# #     return 1400
# # def checkout(request):
# #     return render(request, 'stripe/checkout.html')

# # @csrf_exempt
# # def create_payment(request):
# #     if request.method == 'POST':
# #         try:
# #             data = json.loads(request.body)
# #             # Create a PaymentIntent with the order amount and currency
# #             intent = stripe.PaymentIntent.create(
# #                 amount=calculate_order_amount(data['items']),
# #                 currency='mxn',
# #                 payment_method_types=['card'],
# #             )
# #             return JsonResponse({
# #                 'clientSecret': intent['client_secret']
# #             })
# #         except Exception as e:
# #             return JsonResponse({'error': str(e)}, status=403)
# #     else:
# #         return JsonResponse({'error': 'Method not allowed.'}, status=405)

# # print("create_payment() was executed 111111111")


# # The GET checkout form
# #
# # urlpattern: 
# #   path('checkout', views.checkout, name='checkout'),