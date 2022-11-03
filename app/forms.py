from dataclasses import field
from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from datetime import date

class DateInput(forms.DateInput):
    input_type = 'date'
        
class ContactoForms(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        
        

class ProductoForms(forms.ModelForm):
    fecha_fabricacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    def clean_fecha_fabricacion(self):
        dob = self.cleaned_data['fecha_fabricacion']
        hoy= date.today()
        if (dob.year , dob.month,dob.day) > (hoy.year, hoy.month, hoy.day):
            raise forms.ValidationError('No puedes añadir un libro con fecha futura')
        return dob
    class Meta:
        model = Producto
        fields = '__all__'

        


class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',"first_name", "last_name","email"]
    

class PerfilUsuarioForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_fecha_nacimiento(self):
        dob = self.cleaned_data['fecha_nacimiento']
        hoy= date.today()
        if (dob.year + 18, dob.month,dob.day) > (hoy.year, hoy.month, hoy.day):
            raise forms.ValidationError('Debes tener al menos 18 años')
        return dob
    class Meta:
        model=PerfilUsuario
        fields = ['DNI',"telefono", "genero","fecha_nacimiento",'pais','departamento','ciudad',"generos_preferencia","direccion_correspondencia","foto_perfil"]
        
class ExtendedUserCreationFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name","email"]
        
        
    

class PerfilUsuarioFormUpdate(forms.ModelForm):
    class Meta:
        model=PerfilUsuario
        fields = ["telefono", "genero",'pais','departamento','ciudad',"generos_preferencia","direccion_correspondencia","foto_perfil"]
        
