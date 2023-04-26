from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings 
from django.http.response import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
import stripe
import pdb


from nido.forms import ContactForm
from nido.models import Contact

from django.views.generic.base import TemplateView




stripe.api_key = settings.STRIPE_HOOKS_SECRET
# Create your views here.

# Ejemplo de una pagina con funcion


def test(request):
    template = loader.get_template('nido/test.html')
    context = {
        'aves': ['Quetzal', 'Aguila Arpia', 'Emu', 'Colibri']
    }
    return HttpResponse(template.render(context, request))

# Ejemplo de una pagina simple

def test2(request):
    return render(request, 'nido/test2.html')



# 
# class HomePageView(TemplateView):
#     template_name = 'nido/test.html'
    
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_API_KEY}
#         return JsonResponse(stripe_config, safe=False)



    
# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'GET':
#         domain_url = 'http://localhost:8000/'
#         stripe.api_key = settings.STRIPE_HOOKS_SECRET
#         try:
#             # Create new Checkout Session for the order
#             # Other optional params include:
#             # [billing_address_collection] - to display billing address details on the page
#             # [customer] - if you have an existing Stripe Customer ID
#             # [payment_intent_data] - capture the payment later
#             # [customer_email] - prefill the email input in the form
#             # For full details see https://stripe.com/docs/api/checkout/sessions/create

#             # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#             checkout_session = stripe.checkout.Session.create(
#                 success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
#                 cancel_url=domain_url + 'cancelled/',
#                 payment_method_types=['card'],
#                 mode='payment',
#                 line_items=[
#                     {
#                         'price': '2000',
#                     }
#                 ]
#             )
#             return JsonResponse({'sessionId': checkout_session['id']})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
        
        
        
        
# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = settings.STRIPE_API_KEY
#     endpoint_secret = settings.STRIPE_HOOKS_SECRET
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         print("Payment was successful.")
#         # TODO: run some custom code here

#     return HttpResponse(status=200)

def stripe_index(request):
    stripe.api_key = settings.STRIPE_HOOKS_SECRET
    endpoint_secret = settings.STRIPE_HOOKS_SECRET
    active_products = stripe.Product.list(active=True)
    prices = stripe.Price.list(product=active_products['data'][0]['id'])
    return render(request, 'nido/form_stripe.html', {
        'prices': prices['data'],
    })
    
    
# @csrf_exempt
# def create_checkout_session(request):
#     prices = stripe.Price.list(
#         lookup_keys=[request.POST['lookup_key']],
#         expand=['data.product']
#     )
#     success_url = request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}'
#     cancel_url = request.build_absolute_uri(reverse('cancel'))
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{'price': prices.data[0].id, 'quantity': 1}],
#         mode='subscription',
#         success_url=success_url,
#         cancel_url=cancel_url,
#     )
#     return redirect(checkout_session.url)

YOUR_DOMAIN = 'http://localhost:80/nido'

def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_HOOKS_SECRET
    try:
        prices = stripe.Price.list(
        expand=['data.product']
    )
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': prices.data[0].id, 'quantity': 1}],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            
            
            # line_items=[
            #     {
            #         # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
            #         'price': '{{PRICE_ID}}',
            #         'quantity': 1,
            #     },
            # ],
            # mode='payment',
            # success_url=YOUR_DOMAIN + '/success.html',
            # cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return JsonResponse({'error': str(e)})

    return JsonResponse(checkout_session)

@csrf_exempt
def charge(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        token = request.POST.get('token')
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Example charge',
                source=token,
            )
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            return JsonResponse({'error': e.error.message})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    


# def payment_view(request):
#     test_data = {
#         'amount': 1000,
#         'currency': 'usd',
#         'source': 'tok_visa',
#         'description': 'Test payment',
#     }

#     # Send a test request to the Stripe API
#     response = stripe.Charge.create(**test_data)

#     # Save the response data to your model
#     # ...

#     # Display the response data to the user
#     return render(request, 'payment_test.html', {'response': response})