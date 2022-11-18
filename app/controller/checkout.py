from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import *
import random

@login_required
def index(request):
    rawcart= Carrito.objects.filter(user=request.user)
    for item in rawcart:
        if item.producto_qty > item.product.quantity:
            Carrito.objects.delete(id=item.id)
    
    cartitems=Carrito.objects.filter(user=request.user)
    total_price=0
    for item in cartitems:
        total_price=total_price + item.product.precio * item.producto_qty
    userprofile= PerfilUsuario.objects.filter(user=request.user).first()
    tarjeta=Tarjeta.objects.filter(user=request.user)
    context={'cartitems':cartitems,'total_price':total_price,'userprofile':userprofile,'tarjeta':tarjeta}

    return render(request,"app/checkout.html", context)

@login_required
def placeorder (request):
    if request.method == "POST":

        currentuser = User.objects.filter(id=request.user.id).first()
        if not currentuser.first_name :
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.email = request.POST.get('email')
            currentuser.save()

        

        nuevaorden = Orden()
        nuevaorden.user = request.user
        nuevaorden.fname= request.POST.get('fname')
        nuevaorden.lname= request.POST.get('lname')
        nuevaorden.email= request.POST.get('email')
        nuevaorden.celular= request.POST.get('celular')
        nuevaorden.direccion= request.POST.get('direccion')
        nuevaorden.pais= request.POST.get('pais')
        nuevaorden.ciudad= request.POST.get('ciudad')
        nuevaorden.dni= request.POST.get('dni')
        nuevaorden.fecha_nacimiento= request.POST.get('fecha_nacimiento')
        nuevaorden.forma_pago=request.POST.get('forma_pago')

        carrito = Carrito.objects.filter(user=request.user)
        precio_total_carrito = 0
        for item in carrito:
            precio_total_carrito= precio_total_carrito + item.product.precio * item.producto_qty

        nuevaorden.precio_total = precio_total_carrito
        numtarjeta=int(request.POST.get('forma_pago'))
        print(numtarjeta)
        if (Tarjeta.objects.filter(user=request.user,num_tarjeta=numtarjeta)):

            tarj=Tarjeta.objects.get(user=request.user,num_tarjeta=numtarjeta)


            if(tarj.saldo>= precio_total_carrito):

                tarj.saldo = tarj.saldo - precio_total_carrito
            
                tarj.save()
            else:
                return JsonResponse({'status': "No tienes suficiente saldo"})
        else:
            return JsonResponse({'status': "Tienes que tener una tarejta seleccionada"})
        trackno = 'orden'+str(random.randint(1111111,9999999))

        while Orden.objects.filter(seguimiento_num=trackno) is None:
            trackno = 'orden'+str(random.randint(1111111,9999999))
        
        nuevaorden.seguimiento_num = trackno
        nuevaorden.save()
        nuevaordenitem = Carrito.objects.filter(user=request.user)
        for item in nuevaordenitem:
            OrdenItem.objects.create (
                orden=nuevaorden,
                producto = item.product,
                precio = item.product.precio,
                cantidad = item.producto_qty
            )
            ordenproducto = Producto.objects.filter(id=item.product_id).first()
            ordenproducto.quantity = ordenproducto.quantity - item.producto_qty
            ordenproducto.save()

        Carrito.objects.filter(user=request.user).delete()
        
        messages.success (request, "Tu orden ha sido asignada correctamente")
    

    
    return redirect('/')