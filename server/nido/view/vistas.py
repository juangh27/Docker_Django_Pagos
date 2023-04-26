from django.shortcuts import render
from django.http import HttpResponse




def apadrinamiento(request):
    return render(request, 'vistas/apadrinamiento.html')