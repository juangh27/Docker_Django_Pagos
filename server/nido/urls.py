from django.urls import path

from .view import contact,vistas,stripe
from . import views
from django.views.generic import TemplateView

app_name = 'nido'
urlpatterns = [
    path('test1/', views.test, name='test'),
    path('test2/', views.test2, name='test2'),
    path('apadrinamiento/', vistas.apadrinamiento, name='apadrinamiento'),
    # path('', views.HomePageView.as_view(), name='home'),
    # path('config/', views.stripe_config),
    
    # path('success/', contact.contact, name='success'),
    path('success/', TemplateView.as_view(template_name='nido/success.html'), name='success'),
    path('aves/', TemplateView.as_view(template_name='vistas/aves.html'), name='success'),
    path('base/', TemplateView.as_view(template_name='vistas/base.html'), name='success'),
    
    path('create_checkout_session/', views.create_checkout_session, name='create-checkout-session'),
    path('stripe/', views.stripe_index),
    path('charge/', views.charge, name='charge'),
    path('contact/', contact.contact, name='contact'),
    path('test_api/', contact.payment_test, name='test_payment'),
    path('test_api_payment/', contact.payment_view, name='test_payment_view'),
    # path('checkout/', contact.checkout, name='checkout'),
    path('success2/', contact.success, name='success'),
    path('payment-request/', contact.payment_request_view, name='payment_request_view'),
    path('payment-view/', contact.payment_view_html.as_view(), name='payment_view'),
    path('charge_js/', contact.charge_js, name='charge_js'),
    path('stripe_view/', contact.stripe_js_view.as_view(), name='stripe_js_view'),
    path('test_elemts/', contact.test_elements, name='test_elemts'),
    path('process_payment/', contact.process_payment, name='process_payment'),
    # path('create_payment/', stripe.create_payment, name='create_payment'),
    # path('calculate_order_amount/', stripe.calculate_order_amount, name='calculate_order_amount'),
    path('checkout/', stripe.checkout, name='checkout'),
    path('checkout/create-payment-intent', stripe.create_payment, name='create_payment'),
    
    
]

