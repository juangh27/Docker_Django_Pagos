from django.shortcuts import render, redirect
from nido.forms import ContactForm
from nido.models import Contact


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
