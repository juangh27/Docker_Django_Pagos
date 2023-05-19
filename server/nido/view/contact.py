from django.shortcuts import render, redirect
from nido.forms import PaymentForm, ContactForm
from nido.models import Contact
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.views.generic import TemplateView

@csrf_exempt
@require_POST


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'nido/test_charge.html', {'form': form})



stripe.api_key = settings.STRIPE_HOOKS_SECRET

# def payment_test(request):
#     test_data = {
#         'amount': 1050,
#         'currency': 'mxn',
#         'source': 'tok_visa',
#         'description': 'Test payment pesos',
#     }

#     # Send a test request to the Stripe API
#     response = stripe.Charge.create(**test_data)

#     # Save the response data to your model
#     # ...

#     # Display the response data to the user
#     return render(request, 'nido/payment_form.html', {'response': response})

def payment_test(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Extract payment data from form
            amount = form.cleaned_data['amount']
            # currency = form.cleaned_data['currency']
            # source = form.cleaned_data['source']
            # description = form.cleaned_data['description']
            currency = 'mxn'
            source = 'tok_visa'
            description = form.cleaned_data['description']

            # Send a request to the Stripe API to create a charge
            response = stripe.Charge.create(
                amount=amount,
                currency=currency,
                source=source,
                description=description
            )

            # Handle response data and redirect or render a new template
            # ...
            if response.status == 'succeeded':
                # Redirect to success page
                return redirect('/nido/success')

    else:
        form = PaymentForm()

    return render(request, 'nido/payment_form.html', {'form': form})

def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            card_number = form.cleaned_data['card_number']
            exp_month = form.cleaned_data['exp_month']
            exp_year = form.cleaned_data['exp_year']
            cvc = form.cleaned_data['cvc']

            # Create a Stripe charge
            try:
                charge = stripe.Charge.create(
                    amount=int(amount * 100), # convert to cents
                    currency='usd',
                    source={
                        'number': card_number,
                        'exp_month': exp_month,
                        'exp_year': exp_year,
                        'cvc': cvc,
                    },
                    description='Test Payment',
                )
            except stripe.error.CardError as e:
                # Display error message to user
                return render(request, 'nido/payment_error.html', {'error': e.user_message})

            # Display success message to user
            return render(request, 'nido/payment_success.html', {'amount': amount})

    else:
        form = PaymentForm()
        
    return render(request, 'nido/payment_form.html', {'form': form})

def success(request):
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    payment_intent_id = session.payment_intent
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    amount = payment_intent.amount
    currency = payment_intent.currency
    order_id = payment_intent.metadata.order_id
    # Save the payment details to your database
    return render(request, "nido/success2.html", {
        "amount": amount,
        "currency": currency,
        "order_id": order_id,
    })
    
success_url="http://localhost:8000/nido/success2/?session_id={CHECKOUT_SESSION_ID}"


def checkout(request):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "T-shirt",
                    },
                    "unit_amount": 2000,
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://localhost:8000/nido/success2/",
        cancel_url="http://localhost:8000/nido/cancel/",
        customer_email="test@example.com",
        metadata={"order_id": 1234},
        submit_type="pay",
        locale="auto",
        billing_address_collection="required",
        shipping_address_collection={
            "allowed_countries": ["US", "CA"],
        },
    )
    return redirect(session.url)

def payment_request_view(request):
    supported_payment_methods = [{
        'supportedMethods': 'basic-card',
        'data': {
            'supportedNetworks': ['visa', 'mastercard', 'amex'],
            'supportedTypes': ['debit', 'credit']
        }
    }]
    payment_details = {
        'total': {
            'label': 'Total',
            'amount': {
                'currency': 'USD',
                'value': '10.00'
            }
        }
    }
    payment_options = {
        'requestPayerName': True,
        'requestPayerEmail': True,
        'requestShipping': True,
        'shippingType': 'delivery',
        'buttonCustomization': {
            'style': 'default',
            'label': 'Pay with Card',
            'cssStyles': {
                'color': 'white',
                'backgroundColor': 'blue',
                'borderRadius': '10px',
                'padding': '10px',
                'fontSize': '20px'
            },
            'cssVariables': {
                '--button-background-color': 'blue',
                '--button-text-color': 'white',
                '--button-border-radius': '10px',
                '--button-padding': '10px',
                '--button-font-size': '20px'
            }
        }
    }
    payment_request = {
        'id': 'payment-request-1',
        'methodData': supported_payment_methods,
        'details': payment_details,
        'options': payment_options
    }
    return JsonResponse(payment_request)

class payment_view_html(TemplateView):
    template_name = 'nido/test_view.html'
class stripe_js_view(TemplateView):
    template_name = 'nido/stripe_js.html'
    
def charge_js(request):
    if request.method == "POST":
        # Get the token and amount from the POST data
        token = request.POST.get("token")
        amount = 55555  # $10 in cents

        try:
            # Charge the card using Stripe
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                description="Example charge",
                source=token,
            )

            # Return a success response
            return JsonResponse({"success": True})
        except stripe.error.CardError as e:
            # Return an error response if the card is declined
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return render(request, "nido/stripe_js.html")
    
def test_elements(request):
    if request.method == "POST":
        # Get the token and amount from the POST data
        token = request.POST.get("token")
        amount = 55555  # $10 in cents

        try:
            # Charge the card using Stripe
            charge = stripe.Charge.create(
                amount=amount,
                currency="mxn",
                description="Cargo de ejemplo",
                source=token,
            )

            # Return a success response
            return JsonResponse({"success": True})
        except stripe.error.CardError as e:
            # Return an error response if the card is declined
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return render(request, "stripe/stripe_elements.html")
    
def process_payment(request):
    if request.method == "POST":
        token = request.POST.get("token")
        if token:
            try:
                # Create a new customer with the Stripe token
                customer = stripe.Customer.create(
                    source=token,
                    email=request.user.email
                )
                
                # Save the customer object to your database or update an existing one
                # You can also save the customer ID to your database for future reference
                # For example: request.user.stripe_customer_id = customer.id
                #           request.user.save()
                
                # Return a success response with the customer object
                return JsonResponse({
                    "success": True,
                    "customer": customer
                })
            except stripe.error.CardError as e:
                # Return an error response if there's a problem with the card
                return JsonResponse({
                    "success": False,
                    "error": e.error.message
                })
            except Exception as e:
                # Return an error response if there's a problem with the server
                return JsonResponse({
                    "success": False,
                    "error": str(e)
                })
        else:
            # Return an error response if the token is missing
            return JsonResponse({
                "success": False,
                "error": "Token is missing"
            })