from django.urls import path

from .view import contact
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('tets1/', views.test, name='test'),
    path('test2/', views.test2, name='test2'),
    # path('', views.HomePageView.as_view(), name='home'),
    # path('config/', views.stripe_config),
    
    # path('success/', contact.contact, name='success'),
    path('success/', TemplateView.as_view(template_name='nido/success.html'), name='success'),
    
    path('create-checkout-session/', views.create_checkout_session),
    path('stripe/', views.stripe_index),
    path('charge/', views.charge, name='charge'),
    path('contact/', contact.contact, name='contact')
    
]
