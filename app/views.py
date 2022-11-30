import django
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,permission_required
from django.http import Http404, HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.http.response import JsonResponse
import random
# Create your views here.

def home(request):
    queryset = request.GET.get("buscar")
    productos = Producto.objects.all()
    """ productos = Producto.objects.filter(nombre=True) """
    if queryset:
        productos = Producto.objects.filter(
            Q(nombre__icontains = queryset)|
            Q(nombre__icontains = queryset)|
            Q(precio__icontains = queryset)|
            Q(genero__icontains = queryset)|
            Q(autor__icontains = queryset)
        ).distinct
    data= {
        'productos': productos
    }
    return render(request, 'app/home.html', data)
    

def contacto(request):
    data ={
        'form': ContactoForms()
    }

    if request.method == 'POST':
        formulario = ContactoForms(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]= "Contacto guardado"
        else:
            data["form"]= formulario
            data["mensaje"]= "Error"
    return render(request, 'app/contacto.html',data)

@login_required
def galeria(request):
    return render(request, 'app/galeria.html')

def listar_tarjetas(request):
    tarjetas = Tarjeta.objects.all()
    

    data = {
        'tarjetas': tarjetas,
        'usuario' : request.user,
       
    }
    return render(request, 'app/tarjetas/listar_tarjetas.html',data)


def tarjeta(request):  #TARJETAAAAAAAAA
    data={
        'usuario': request.user
    }
    if request.method == 'POST':
        if request.user.is_authenticated:
            num_tarjeta_p= int(request.POST.get("num_tarjeta"))
            nombre_propietario_p= str(request.POST.get("nombre_propietario"))
            mes_exp_p= int(request.POST.get("mes_exp"))
            year_exp_p= int(request.POST.get("year_exp"))
            cvv_p= int(request.POST.get("cvv"))
            saldo_p= int(request.POST.get("saldo"))
            
            
            Tarjeta.objects.create(user=request.user, num_tarjeta=num_tarjeta_p , nombre_propietario = nombre_propietario_p, mes_exp=mes_exp_p ,year_exp=year_exp_p, cvv=cvv_p, saldo=saldo_p)

            messages.success(request,"Tarjeta agregada")
            return redirect(to="listar_tarjetas")
   
   
    return render(request, 'app/tarjetas/tarjeta.html',data)


def agregar_saldo(request,id):
    tarjeta = get_object_or_404 (Tarjeta , id=id)
    saldo_actual=tarjeta.saldo 
    data={
        'tarjeta': tarjeta,
        'usuario': request.user
    }
    if request.method == 'POST':
        saldo_nuevo= int(request.POST.get("saldo"))

        saldo = Tarjeta.objects.get(id=tarjeta.id,user=request.user)
        saldo.saldo = saldo_nuevo + saldo_actual
        saldo.save()
      
    
        messages.success(request,"Se ha agregado saldo a tu tarjeta")
        return redirect(to="listar_tarjetas")
    
    return render(request,'app/tarjetas/agregar_saldo.html',data)

def eliminar_tarjeta(request, id):

    tarjeta = get_object_or_404(Tarjeta, id=id)
    tarjeta.delete()
    messages.warning(request,"Tarjeta eliminada")
    return redirect(to="ver_perfil")

@permission_required('app.add_producto')
def agregar_producto(request):
    editorial=Editorial.objects.all()
    data={
        'editorial': editorial
    }
    if request.method == 'POST':
        producto=Producto()
        producto.nombre= str(request.POST.get("nombre_libro"))
        producto.precio= int(request.POST.get("precio_libro"))
        producto.autor= str(request.POST.get("autor_libro"))
        producto.genero= int(request.POST.get("generos"))
        producto.num_paginas= int(request.POST.get("num_paginas"))
        producto.descripcion= str(request.POST.get("descripcion_libro"))
        producto.nuevo= bool(request.POST.get("nuevo"))
        editorial_libro= request.POST.get("editorial_libro")
        producto.fecha_fabricacion= request.POST.get("fecha_fabricacion")
        producto.issn= int(request.POST.get("issn_libro"))
        producto.quantity= int(request.POST.get("cantidad_libro"))
        producto.editorial=Editorial.objects.get(nombre=editorial_libro)
        producto.save()
        
        noticia.objects.create(producto=producto)
        messages.success(request,"Libro agregado")

        return redirect(to="/")


    return render(request,'app/producto/agregar.html',data)

@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(productos,5)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator':paginator,
    }

    return render(request,'app/producto/listar.html',data)

@permission_required('app.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoFormsUpdate(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoFormsUpdate(data = request.POST,instance=producto, files = request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Editado correctamente")
            return redirect(to="listar_productos")
        else:
            data["form"]= formulario
            data["mensaje"]= "Error de gurdado"

    return render(request,'app/producto/modificar.html',data)

@permission_required('app.delete_producto')
def eliminar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.warning(request,"Eliminado correctamente")
    return redirect(to="listar_productos")

class DetalleLibro(generic.detail.DetailView):
    model= Producto
    template_name= 'app/producto/librodetalle.html'


def agregar_tienda(request):

    data={
        'form': TiendaForms()
    }
    if request.method == 'POST':
        formulario = TiendaForms(data = request.POST, files = request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Tienda registrada")
            return redirect(to="listar_tiendas")
        else:
            data["form"]= formulario
            data["mensaje"]= "Error de guardado"


    return render(request,'app/tienda/agregar.html',data)

@permission_required('app.view_tienda')
def listar_tiendas(request):
    tiendas = Tienda.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(tiendas,5)
        tiendas = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': tiendas,
        'paginator':paginator,
    }

    return render(request,'app/tienda/listar.html',data)

@permission_required('app.change_tienda')
def modificar_tienda(request, id):

    tienda = get_object_or_404(Tienda, id=id)

    data = {
        'form': TiendaForms(instance=tienda)
    }
    if request.method == 'POST':
        formulario = TiendaForms(data = request.POST,instance=tienda, files = request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Editada correctamente")
            return redirect(to="listar_tiendas")
        else:
            data["form"]= formulario
            data["mensaje"]= "Error de gurdado"

    return render(request,'app/tienda/modificar.html',data)

@permission_required('app.delete_tienda')
def eliminar_tienda(request, id):

    tienda = get_object_or_404(Tienda, id=id)
    tienda.delete()
    messages.warning(request,"Eliminada correctamente")
    return redirect(to="listar_tiendas")

def recoger_tienda(request):
    tiendas = Tienda.objects.all()

    
    page = request.GET.get('page',1)
    cartitems=Carrito.objects.filter(user=request.user)
    try:
        paginator = Paginator(tiendas,10)
        tiendas = paginator.page(page)
    except:
        raise Http404

    data = {
        
        'paginator':paginator,

        'carrito': cartitems,
        'entity': tiendas
    }

    return render(request,'app/listarrecogertienda.html',data)
    
def checkout_tienda(request,id):
    rawcart= Carrito.objects.filter(user=request.user)
    for item in rawcart:
        if item.producto_qty > item.product.quantity:
            Carrito.objects.delete(id=item.id)
    
    cartitems=Carrito.objects.filter(user=request.user)
    total_price=0
    for item in cartitems:
        total_price=total_price + item.product.precio * item.producto_qty
    
    tienda=get_object_or_404 (Tienda , id=id)
    
    userprofile= PerfilUsuario.objects.filter(user=request.user).first()
    tarjeta=Tarjeta.objects.filter(user=request.user)
    context={'cartitems':cartitems,'total_price':total_price,'userprofile':userprofile,'tarjeta':tarjeta,'tienda':tienda}

    return render(request,"app/checkout_tienda.html", context)


def checkout_tienda_orden(request,id):
    tienda=get_object_or_404 (Tienda , id=id)
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
            print(item.product.nombre)
            OrdenItem.objects.create (
                orden=nuevaorden,
                producto = item.product,
                precio = item.product.precio,
                cantidad = item.producto_qty
            )

            
            existenciaproducto = Existencias.objects.filter(producto=item.product,tienda=tienda).first()
            existenciaproducto.existencias = existenciaproducto.existencias - item.producto_qty
            print(existenciaproducto.existencias)
            existenciaproducto.save()

        Carrito.objects.filter(user=request.user).delete()
        
        messages.success (request, "Tu orden ha sido asignada correctamente")
    

    
        return redirect('/')

def agregar_existencias(request,id,id2):
    tienda = get_object_or_404 (Tienda , id=id)
    producto = get_object_or_404 (Producto , id=id2)
    data={
        'form': ExistenciasForms(),
        'tienda': tienda,
        'producto': producto
    }
    if request.method == 'POST':
        existencias_cant= int(request.POST.get("existencias"))
        if (existencias_cant > producto.quantity):
            #messages.error(request, "Cagaste")
            return JsonResponse({'status': "No puedes agregar más existencias de las que hay"})
        
        if(Existencias.objects.filter(producto=producto, tienda=tienda)):
            return JsonResponse({'status': "Ya esta este libro en esta tienda"})

        else:
            producto.quantity = producto.quantity - existencias_cant
            producto.save()
            print(producto.quantity)
            Existencias.objects.create(producto=producto,tienda=tienda,existencias=existencias_cant)
            messages.success(request,"Existencia registrada")
            return redirect(to="listar_tiendas")
    
    return render(request,'app/existencias/agregar.html',data)


def aumentar_existencias_t(request,id,id2,id3):
    tienda = get_object_or_404 (Tienda , id=id)
    producto = get_object_or_404 (Producto , id=id2)
    existencia = get_object_or_404 (Existencias , id=id3)
    existencia_seleccionada = existencia.existencias
    data={
        'form': ExistenciasForms(),
        'tienda': tienda,
        'producto': producto
    }
    if request.method == 'POST':
        existencias_cant= int(request.POST.get("existencias"))

        if (existencias_cant > producto.quantity):
            #messages.error(request, "Cagaste")
            return JsonResponse({'status': "No puedes agregar más existencias de las que hay"})
        

        else:
            producto.quantity = producto.quantity - existencias_cant
            
            producto.save()
            exis = Existencias.objects.get(producto=producto, tienda=tienda)
            exis.existencias = existencias_cant + existencia_seleccionada
            exis.save()
            print(producto.quantity)
           
            messages.success(request,"Existencia actualizada")
            return redirect(to="listar_tiendas")
    
    return render(request,'app/existencias/agregar.html',data)

def eliminar_existencias_t(request,id,id2,id3):
    tienda = get_object_or_404 (Tienda , id=id)
    producto = get_object_or_404 (Producto , id=id2)
    existencia = get_object_or_404 (Existencias , id=id3)
    existencia_seleccionada = existencia.existencias
    data={
        'form': ExistenciasForms(),
        'tienda': tienda,
        'producto': producto
    }
    if request.method == 'POST':
        existencias_cant= int(request.POST.get("existencias"))

        if (existencias_cant >= existencia_seleccionada):
            existencia.delete()
            messages.success(request,"Existencia Eliminada")
            return redirect(to="listar_tiendas")
        

        else:
            producto.quantity = producto.quantity + existencias_cant
            
            producto.save()
            exis = Existencias.objects.get(producto=producto, tienda=tienda)
            exis.existencias = existencia_seleccionada - existencias_cant
            exis.save()
            print(producto.quantity)
           
            messages.success(request,"Existencia actualizada")
            return redirect(to="listar_tiendas")
    
    return render(request,'app/existencias/agregar.html',data)


def escoger_existencias(request,id):
    tienda = get_object_or_404(Tienda, id=id)
    libros = Producto.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(libros,5)
        libros = paginator.page(page)
    except:
        raise Http404

    data = {
        'tienda' : tienda,
        'entity': libros,
        'paginator':paginator,
    }

    return render(request,'app/existencias/escoger_existencia.html',data)

def listar_existencias(request,id):
    existencias = Existencias.objects.all()
    tienda = get_object_or_404(Tienda, id=id)
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(existencias,10)
        existencias = paginator.page(page)
    except:
        raise Http404

    data = {
        'existencias': existencias,
        'tienda' : tienda,
        'paginator':paginator,
    }

    return render(request,'app/existencias/listar.html',data)

def listar_noticias(request):
    noticias = noticia.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(noticias,5)
        noticias = paginator.page(page)
    except:
        raise Http404

    data = {
        'noticia': noticias,
        'paginator':paginator,
    }

    return render(request,'app/noticia.html',data)

def eliminar_noticia(request, id):

    noticias = get_object_or_404(noticia, id=id)
    noticias.delete()
    messages.warning(request,"Eliminada correctamente")
    return redirect(to="listar_noticias")

def mapa(request):
    tiendas = Tienda.objects.all()
    page = request.GET.get('page',1)
    try:
        paginator = Paginator(tiendas,5)
        tiendas = paginator.page(page)
    except:
        raise Http404
    data = {
        'entity': tiendas,
        'paginator':paginator,
    }
    return render(request,'app/tienda/mapa.html',data)

def ver_perfil(request):
    data = {
        'user': request.user
    }
  
    
    return render(request, 'app/perfil/verperfil.html',data)


@login_required
def modificar_perfil(request):
    if request.method == 'POST':
        formulario = ExtendedUserCreationFormUpdate( request.POST,instance=request.user)
        perfil_formulario = PerfilUsuarioFormUpdate(request.POST,request.FILES, instance=request.user.perfilusuario)
    
        if formulario.is_valid() and perfil_formulario.is_valid():
            formulario.save()
            perfil_formulario.save()
            messages.success(request, "Editado correctamente")
            return redirect(to="home")

    else:
        formulario = ExtendedUserCreationFormUpdate(instance=request.user)
        perfil_formulario = PerfilUsuarioFormUpdate(instance=request.user.perfilusuario)
    
    data = {
        'form': formulario,
        'perfil_form': perfil_formulario
    }
    return render(request,'app/perfil/modificarperfil.html',data)



class eliminar_perfil(generic.DeleteView):
    model = User
    template_name="app/perfil/eliminarperfil.html"
    success_url = reverse_lazy('home')

class cambiar_contrasenia (PasswordChangeView):
    template_name="app/perfil/cambiarcontraseña.html"
    success_url = reverse_lazy('ver_perfil')
def registro(request):
    data = {
        'form': ExtendedUserCreationForm,
        'perfil_form': PerfilUsuarioForm
        }
    if request.method == 'POST':
        formulario = ExtendedUserCreationForm(data=request.POST,files = request.FILES)
        perfil_formulario = PerfilUsuarioForm(data=request.POST,files = request.FILES)
        if formulario.is_valid() and perfil_formulario.is_valid():
            user = formulario.save()
            perfil = perfil_formulario.save(commit=False)
            perfil.user= user
            perfil.save()
            user_group = Group.objects.get(name='Cliente') 
            user.groups.add(user_group)
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request, " Te has registrado correctamente")
            return redirect(to="home")
        
        data["form"] = formulario
        data["perfil_form"]=perfil_formulario
    return render(request, 'registration/registro.html', data)



def forums(request):
    forums=forum.objects.all()
    count=forums.count()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())

    context={'forums':forums,
              'count':count,
              'discussions':discussions}
    return render(request,'app/forum.html',context)

def addInForum(request):
    usuario=request.user
    if request.method == 'POST':
        if request.user.is_authenticated:
            tema_foro= str(request.POST.get("tema"))
            descripcion_foro= str(request.POST.get("descripcion"))
            print(tema_foro)
            forum.objects.create(user=request.user, tema=tema_foro, descripcion=descripcion_foro)

            messages.success(request,"Tu tema ha sido registrado!")
            
            return redirect(to="forum")

    context ={'usuario':usuario}
    return render(request,'app/addInForum.html',context)

def addInDiscussion(request,id):
    respuesta_a =get_object_or_404(forum,id=id)
    
    if request.method == 'POST':
        discussion= str(request.POST.get("tema"))
    
        Discussion.objects.create(forum=respuesta_a, discuss=discussion, user=request.user)
        messages.success(request,"Tu respuesta ha sido registrada!")
            
        return redirect(to="forum")

    context ={'respuesta':respuesta_a}
    return render(request,'app/addInDiscussion.html',context)
