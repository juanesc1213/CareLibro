from dataclasses import field
from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'
        
class ContactoForms(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        
        

class ProductoForms(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

        widgets ={
            "fecha_fabricacion": DateInput(),
        }


class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',"first_name", "last_name","email"]
    

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model=PerfilUsuario
        fields = ['DNI',"telefono", "genero","fecha_nacimiento","lugar_nacimiento","generos_preferencia","direccion_correspondencia"]
        widgets = {
            'fecha_nacimiento': DateInput(),
        }

class ExtendedUserCreationFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name","email"]
        
        
    

class PerfilUsuarioFormUpdate(forms.ModelForm):
    class Meta:
        model=PerfilUsuario
        fields = ["telefono", "genero","lugar_nacimiento","generos_preferencia","direccion_correspondencia"]

class CreateInForum(ModelForm):
    class Meta:
        model= forum
        fields = "__all__"

class CreateInDiscussion(ModelForm):
    class Meta:
        model= Discussion
        fields = "__all__"
        
