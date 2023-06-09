
# Create your models here.
from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class test(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()

    class Meta:
        verbose_name = 'my model'


class Product_test(models.Model):
    product_name = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.product_name
    
class Product_price(models.Model):
    product = models.ForeignKey(Product_test, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0) 
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
    

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    
class ChargeForm(models.Model):
    amount = models.IntegerField()
    token = models.CharField(max_length=252)
    

class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.CharField(max_length=500)
    
class PaymentForm(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    card_number = models.CharField(max_length=16)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    cvc = models.IntegerField()
    
class DonationOption(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    
class DonationOption1(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    info = models.CharField(max_length=500)
    aves = models.CharField(max_length=255)
    entradas = models.CharField(max_length=255)
