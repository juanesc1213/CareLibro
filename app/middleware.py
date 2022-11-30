import datetime
from datetime import timedelta
from app.models import Reserva, Orden
from django.utils import timezone
now = timezone.now()
class PruebaMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        #print(response.user)
        return response

    def process_view(self,request, view_func, view_args, view_kwargs):
        
        if request.user.is_authenticated:
            fecha_actual = datetime.date.today()
            reservas = Reserva.objects.filter(estado=True, user=request.user)
            for reserva in reservas:
                fecha_vencimiento = reserva.fecha_creacion + timedelta(days=1)
                
                if fecha_actual >= fecha_vencimiento:
                    print("si se pudo")
                    
                    reserva.estado = False
                    reserva.delete()


class PruebaMiddlewareCompra:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self,request,view_func,view_args,view_kwargs):
        if request.user.is_authenticated:
            fecha_actual = datetime.datetime.today()
            compras = Orden.objects.filter(estatus='Pendiente', user=request.user)
            
            for reserva in compras:
                fecha_vencimiento = reserva.creado_en + timedelta(days=3)
                print(fecha_vencimiento)
                if now > fecha_vencimiento and reserva.estatus == 'Pendiente':
                    print('Fecha actual es mayor que la de creacion')
                    reserva.estatus = 'Completado'
                    reserva.save()