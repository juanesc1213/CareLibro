from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages 


from app.models import Carrito, Producto

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