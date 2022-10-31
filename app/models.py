from ast import Delete
from distutils.command.upload import upload
from random import choices
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator

# Create your models here.
GENEROS_PREFERENCIA = ((1, 'Accion'),
              (2, 'Aventura'),
              (3, 'Terror'),
              (4, 'Ciencia Ficcion'),
              (5, 'Romance'),
              (6, 'Humor'),
              (7, 'Poesia'),
              (8, 'Novela'))


class Editorial(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre =                models.CharField(max_length=50)
    precio =                models.IntegerField()
    autor =                 models.CharField(max_length=50)
    genero =                models.IntegerField(choices=GENEROS_PREFERENCIA)
    num_paginas=            models.IntegerField()
    descripcion =           models.TextField()
    nuevo =                 models.BooleanField()
    editorial =             models.ForeignKey(Editorial, on_delete=models.PROTECT)
    fecha_fabricacion =     models.DateField()
    issn=                   models.IntegerField(unique = True)
    imagen =                models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.nombre

opciones_consulta =[
    [0, "consulta"],
    [1, "reclamo"],
    [2, "sugerencia"],
    [3, "felicitaciones"],
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre

GENEROS_PREFERENCIA = ((1, 'Accion'),
              (2, 'Aventura'),
              (3, 'Terror'),
              (4, 'Ciencia Ficcion'),
              (5, 'Romance'),
              (6, 'Humor'),
              (7, 'Poesia'),
              (8, 'Novela'))

GENERO =(
    (1, "Masculino"),
    (2, "Femenino"),
    (3, "No binario"),
)
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    DNI = models.PositiveIntegerField(primary_key=True, unique=True,validators=[MaxValueValidator(9999999999)])
    telefono = models.IntegerField()
    genero=models.IntegerField(choices=GENERO)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = CountryField()
    generos_preferencia = MultiSelectField(choices=GENEROS_PREFERENCIA,max_length=100)
    direccion_correspondencia = models.CharField(max_length=100)
    

    def __str__(self):
        return self.user.username