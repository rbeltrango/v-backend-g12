from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .serializers import PruebaSerializers, TareaSerializer
from .models import Tareas

@api_view(http_method_names=['GET','POST'])
def inicio(request: Request):
    # request sera toda la informacion enviada por el cliente > https://www.django-rest-framework.org/api-guide/requests/
    print(request.method)
    print(request)
    if request.method=='GET':
    # comportamiento cuando sea GET
        return Response(data={
            'message':'bienvenido a mi API de agenda'
        })

    elif request.method=='POST':
    # comportamiento cuando sea POST
        return Response(data={
            'message':'hiciste el post'
        }, status=201)
        
class PruebaApiView(ListAPIView):
    serializer_class=PruebaSerializers


    queryset = [{
        'nombre':'Eduardo', 
        'apellido': 'De Rivero', 
        'correo':'ederiv@gmail.com',
        'dni':'73500746', 
        'estado_civil':'viudo'},
        {
        'nombre':'maria', 
        'apellido': 'perez', 
        'correo':'ederiv@gmail.com',
        'dni':'73500746', 
        'estado_civil':'casado'}]

    def get(self, request:Request):
        informacion=self.queryset

        informacion_serializada=self.serializer_class(data=informacion, many=True)

        informacion_serializada.is_valid(raise_exception=True)
        return Response(data={
            'message':'Hola',
            'content': informacion_serializada.data
            })
    
class TareasApiView(ListCreateAPIView):
    queryset=Tareas.objects.all() # SELECT * from TAREAS
    serializer_class=TareaSerializer

