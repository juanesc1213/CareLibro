import django
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,permission_required
from django.http import Http404
from .models import *
from .forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

# Create your views here.

def home(request):
    productos = Producto.objects.all()
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

@permission_required('app.add_producto')
def agregar_producto(request):

    data={
        'form': ProductoForms()
    }
    if request.method == 'POST':
        formulario = ProductoForms(data = request.POST, files = request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Producto Registrado")
        else:
            data["form"]= formulario
            data["mensaje"]= "Error de guardado"


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
        'form': ProductoForms(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForms(data = request.POST,instance=producto, files = request.FILES)
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
        formulario = ExtendedUserCreationForm(data=request.POST)
        perfil_formulario = PerfilUsuarioForm(data=request.POST)
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