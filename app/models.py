from ast import Delete
from distutils.command.upload import upload
from random import choices
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator
from cities_light.models import Country, Region, City
from smart_selects.db_fields import ChainedForeignKey
# Create your models here.
GENEROS_PREFERENCIA = ((1, 'Accion'),
              (2, 'Aventura'),
              (3, 'Terror'),
              (4, 'Ciencia Ficcion'),
              (5, 'Romance'),
              (6, 'Humor'),
              (7, 'Poesia'),
              (8, 'Novela'))

DIAS_SEMANA = ((1, 'Lunes'),
              (2, 'Martes'),
              (3, 'Miercoles'),
              (4, 'Jueves'),
              (5, 'Viernes'),
              (6, 'Sabado'),
              (7, 'Domingo'))

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
    quantity =              models.IntegerField(null=True)

    def __str__(self):
        return self.nombre

opciones_consulta =[
    [0, "consulta"],
    [1, "reclamo"],
    [2, "sugerencia"],
    [3, "felicitaciones"],
]
class Tienda (models.Model):
    nombre =                models.CharField(max_length=50)
    dias_atencion =         MultiSelectField(choices=DIAS_SEMANA,max_length=100)
    telefono =              models.IntegerField()
    horario_apertura =      models.TimeField()
    horario_cierre =        models.TimeField()

    def __str__(self):
        return self.nombre

class Carrito (models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Producto, on_delete = models.CASCADE)
    producto_qty = models.IntegerField(null=False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

class Existencias(models.Model):
    producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    tienda = models.ForeignKey(Tienda, on_delete = models.CASCADE)
    existencias= models.IntegerField(null= True)


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
    pais = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    departamento = ChainedForeignKey(Region, chained_field="pais", chained_model_field="country", null=True)
    ciudad = ChainedForeignKey(City, chained_field="departamento", chained_model_field="region", null=True)
    generos_preferencia = MultiSelectField(choices=GENEROS_PREFERENCIA,max_length=100,null=True,blank=True)
    direccion_correspondencia = models.CharField(max_length=100, null=True,blank=True)
    foto_perfil = models.ImageField(upload_to="fotoperfil", null=True, blank=True)

    def __str__(self):
        return self.user.username

class Tarjeta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_tarjeta = models.IntegerField()
    nombre_propietario = models.CharField(max_length=50,null=True)
    mes_exp = models.IntegerField()
    year_exp = models.IntegerField()
    cvv = models.IntegerField()
    saldo = models.IntegerField()

class forum(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    tema= models.CharField(max_length=300)
    descripcion = models.CharField(max_length=1000,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    

class noticia(models.Model):
    producto=               models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion =           models.TextField(null=True,blank=True)
    fecha_publicacion =     models.DateTimeField(auto_now_add=True, null=True)


#child model
class Discussion(models.Model):
    forum = models.ForeignKey(forum,blank=True,on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    user= models.ForeignKey(User,on_delete=models.CASCADE, null=True)

class Orden(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    fname=models.CharField(max_length=150, null=True)
    lname=models.CharField(max_length=150, null=True)
    email=models.CharField(max_length=150, null=True)
    celular=models.CharField(max_length=150, null=True)
    direccion=models.TextField( null=True)
    pais=models.CharField(max_length=150, null=True)
    ciudad=models.CharField(max_length=150, null=True)
    dni=models.CharField(max_length=150, null=True)
    fecha_nacimiento=models.CharField(max_length=150, null=True)
    precio_total = models.FloatField(null=True)
    forma_pago = models.CharField(max_length=150, null=True)
    forma_pago_id = models.CharField(max_length=150, null=True)
    statusdeorden = {
        ('Pendiente','Pendiente'),
        ('En envio','En envio'),
        ('Completado','Completado'),
        ('Cancelada','Cancelada'),
        ('Devuelta','Devuelta'),
        
    }
    estatus = models.CharField(max_length=150,choices=statusdeorden,default ='Pendiente')
    mensaje =models.TextField( null=True)
    seguimiento_num = models.CharField(max_length=150, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.seguimiento_num)

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete = models.CASCADE)
    producto =models.ForeignKey(Producto, on_delete = models.CASCADE)
    precio = models.FloatField(null=True)
    cantidad = models.IntegerField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.orden.id, self.orden.seguimiento_num)

class Reserva(models.Model):
    product = models.ForeignKey(Producto, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    cantidad_dias = models.SmallIntegerField('Cantidad de dias a reservar',default=1)
    fecha_creacion = models.DateField(auto_now_add=True)
    cantidad_producto= models.IntegerField(null=True)
    estado = models.BooleanField(default=True,verbose_name='Estado')