from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from app.models import Carrito

def index(request):
    rawcart= Carrito.objects.filter(user=request.user)
    for item in rawcart:
        if item.producto_qty > item.product.quantity:
            Carrito.objects.delete(id=item.id)
    
    cartitems=Carrito.objects.filter(user=request.user)
    total_price=0
    for item in cartitems:
        total_price=total_price + item.product.precio * item.producto_qty

    context={'cartitems':cartitems,'total_price':total_price}

    return render(request,"app/checkout.html", context)