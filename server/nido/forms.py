from django import forms
from django.core.validators import DecimalValidator

class ChargeForm(forms.Form):
    amount = forms.IntegerField()
    token = forms.CharField()
    

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
class PaymentForm(forms.Form):
    amount = forms.DecimalField(min_value=10, max_value=6000, validators=[DecimalValidator(max_digits=8, decimal_places=2)], widget=forms.NumberInput(attrs={'min': '10.00', 'step': '0.01'}))
    card_number = forms.CharField(max_length=30)
    exp_month = forms.IntegerField(min_value=1, max_value=12)
    exp_year = forms.IntegerField(min_value=2023, max_value=2050)
    cvc = forms.IntegerField(min_value=100, max_value=999)
    description = forms.CharField(max_length=1000)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        amount = int(amount * 100)  # Convert decimal value to integer value
        return amount