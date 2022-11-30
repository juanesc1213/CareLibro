from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages 


from app.models import Carrito, Producto, PerfilUsuario,Reserva

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Producto.objects.get(id=prod_id)
            if(product_check):
                
                
                if(Carrito.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': "el Libro ya está en el carrito"})
                else:
                    prod_qty = int(request.POST.get('producto_qty'))

                    if product_check.quantity >= prod_qty :
              
                        Carrito.objects.create(user=request.user, product_id=prod_id, producto_qty=prod_qty)
                        return JsonResponse({'status': "Libro añadido exitosamente  "})
                    else:
                        return JsonResponse({'status': "Sólo hay "+ str(product_check.quantity)+ " unidades disponibles"})

            else:
                return JsonResponse({'status': "No se encontró el producto"}) 
        else:
            """ return print("login necesario") """
            return JsonResponse({'status': "Login para continuar"}) 

    return redirect('/')

def viewcart(request):
    cart = Carrito.objects.filter(user=request.user)
    
    context = {'cart':cart}
    return render(request, "app/cart.html", context)


def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Carrito.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('producto_qty'))
            cart = Carrito.objects.get(product_id=prod_id, user=request.user)
            cart.producto_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Actualizado exitosamente"})
    return redirect('/')

def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Carrito.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Carrito.objects.get(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status':"Eliminado exitosamente"})
    return redirect('/')

def RegistrarReserva(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Producto.objects.get(id=prod_id)
            conteo=Reserva.objects.filter(user=request.user).count()
            print(conteo)
            if(product_check):
                
                if(Reserva.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': "Este libro ya ha sido reservado"})
                if (conteo>2):
                    return JsonResponse({'status': "No puedes reservar más de 3 libros diferentes"})                
                else:
                    prod_qty = int(request.POST.get('producto_qty'))

                    if product_check.quantity >= prod_qty :
                        product_check.quantity =  product_check.quantity -prod_qty
                        Reserva.objects.create(product_id=prod_id,user=request.user, cantidad_producto=prod_qty)
                        product_check.save()
                        return JsonResponse({'status': "Libro reservado exitosamente  "})
                    else:
                        return JsonResponse({'status': "Sólo hay "+ str(product_check.quantity)+ " unidades disponibles"})

            else:
                return JsonResponse({'status': "No se encontró el producto"}) 
        else:
            """ return print("login necesario") """
            return JsonResponse({'status': "Login para continuar"}) 

    return redirect('/')
def addtocartReserva(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Producto.objects.get(id=prod_id)
            if(product_check):                
                if(Carrito.objects.filter(user=request.user.id, product_id=prod_id) and Reserva.objects.filter(user=request.user.id,product_id=prod_id)):
                    carrito=Carrito.objects.filter(user=request.user.id, product_id=prod_id).first()
                    reserva=Reserva.objects.filter(user=request.user.id, product_id=prod_id).first()
                    print('reserva',reserva.cantidad_producto)
                    carrito.producto_qty=carrito.producto_qty + reserva.cantidad_producto
                    product_check.quantity = product_check.quantity + reserva.cantidad_producto
                    product_check.save()
                    print('reserva',carrito.producto_qty)
                    carrito.save()
                    reserva.delete()
                    return JsonResponse({'status': "Libro añadido exitosamente  "})
                else:
                    prod_qty = int(request.POST.get('producto_qty'))

                    if product_check.quantity >= prod_qty :
                        reserva=Reserva.objects.filter(user=request.user.id, product_id=prod_id).first()
                        product_check.quantity = product_check.quantity + reserva.cantidad_producto
                        product_check.save()
                        reserva.delete()
                        
                        Carrito.objects.create(user=request.user, product_id=prod_id, producto_qty=prod_qty)
                        return JsonResponse({'status': "Libro añadido exitosamente  "})
                    else:
                        return JsonResponse({'status': "Sólo hay "+ str(product_check.quantity)+ " unidades disponibles"})

            else:
                return JsonResponse({'status': "No se encontró el producto"}) 
        else:
            """ return print("login necesario") """
            return JsonResponse({'status': "Login para continuar"}) 

    return redirect('/')
def viewreserva(request):
    reserva = Reserva.objects.filter(user=request.user)
    
    context = {'reserva':reserva}
    return render(request, "app/reserva.html", context)

def deletereservaitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Reserva.objects.filter(user=request.user, product_id=prod_id)):
            reserva= Reserva.objects.get(product_id=prod_id, user=request.user)
            product_check = Producto.objects.get(id=prod_id)
            product_check.quantity = reserva.cantidad_producto + product_check.quantity
            product_check.save()
            reserva.delete()
        return JsonResponse({'status':"Eliminado exitosamente"})
    return redirect('/')