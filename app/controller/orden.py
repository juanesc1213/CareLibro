from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models import *
from datetime import timedelta
from django.utils import timezone
now = timezone.now()
def index(request):
    ordenes = Orden.objects.filter(user=request.user)
    
    context={'orden':ordenes}
    return render(request, 'app/ordenes/index.html',context)

def verorden(request, t_no):
    orden = Orden.objects.filter(seguimiento_num=t_no).filter(user=request.user).first()
    fecha_vencimiento = orden.creado_en + timedelta(days=7)
    if now < fecha_vencimiento:
        fecha= fecha_vencimiento
    else:
        fecha=orden.creado_en

    ordenitems= OrdenItem.objects.filter(orden=orden)
    context={'orden':orden,'ordenitem':ordenitems,"tiempo":fecha}
    return render(request, 'app/ordenes/view.html',context)

def cancelar_orden(request, t_no):
    orden = Orden.objects.filter(seguimiento_num=t_no).filter(user=request.user).first()
    num_tarjeta_orden=int(orden.forma_pago)
    tarjeta= Tarjeta.objects.filter(user=request.user,num_tarjeta=num_tarjeta_orden).first()
    orden.estatus = 'Cancelada'
    tarjeta.saldo = tarjeta.saldo + orden.precio_total
    orden.save()
    tarjeta.save()
    itemordenes=OrdenItem.objects.filter(orden=orden)
    for item in itemordenes:
            ordenproducto = Producto.objects.filter(id=item.producto_id).first()
            ordenproducto.quantity = ordenproducto.quantity + item.cantidad
            ordenproducto.save()

    messages.warning(request,"Compra Cancelada")
    return redirect(to="ordenes")

def realizar_devolucion(request,t_no):
    orden = Orden.objects.filter(seguimiento_num=t_no).filter(user=request.user).first()
    num_tarjeta_orden=int(orden.forma_pago)
    mi_tarjeta= Tarjeta.objects.filter(user=request.user,num_tarjeta=num_tarjeta_orden).first()
    orden.estatus = 'Devuelta'
    mi_tarjeta.saldo = mi_tarjeta.saldo + orden.precio_total
    orden.save()
    mi_tarjeta.save()
    itemordenes=OrdenItem.objects.filter(orden=orden)
    for item in itemordenes:
            ordenproducto = Producto.objects.filter(id=item.producto_id).first()
            ordenproducto.quantity = ordenproducto.quantity + item.cantidad
            ordenproducto.save()
    if request.method == "POST":
        messages.warning(request,"Tu compra ha sido devuelta")
        return redirect(to="ordenes")
    data = {'orden':orden}
    return render(request,'app/devolucion.html',data)
    