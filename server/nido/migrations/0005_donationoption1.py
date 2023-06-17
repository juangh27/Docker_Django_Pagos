# Generated by Django 4.1.7 on 2023-06-17 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nido', '0004_donationoption'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationOption1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('info', models.CharField(max_length=500)),
                ('aves', models.CharField(max_length=255)),
                ('entradas', models.CharField(max_length=255)),
            ],
        ),
    ]
