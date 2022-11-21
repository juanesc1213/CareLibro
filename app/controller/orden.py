from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import *

def index(request):
    ordenes = Orden.objects.filter(user=request.user)
    context={'orden':ordenes}
    return render(request, 'app/ordenes/index.html',context)

def verorden(request, t_no):
    orden = Orden.objects.filter(seguimiento_num=t_no).filter(user=request.user).first()
    ordenitems= OrdenItem.objects.filter(orden=orden)
    context={'orden':orden,'ordenitem':ordenitems}
    return render(request, 'app/ordenes/view.html',context)
