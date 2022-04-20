from pytz import timezone
from .models import Plato, Stock
from rest_framework.generics import CreateAPIView, ListCreateAPIView,CreateAPIView
from .serializer import AgregarDetallePedidoSerializer, PedidosSerializer, PlatoSerializer, StockSerializer
from rest_framework.permissions import (
AllowAny, # sirve para que el controlador se pubilco
IsAuthenticated, # los controladores soliciten una token de acceso
IsAuthenticatedOrReadOnly, # sólo para los métodos get no será necesario la token pero para (POST, PUT,DELETE,PATCH SÍ será requerido)
IsAdminUser, # verifica que en la token de acceso buscará al usuario y verá si es superuser (is_superuser)
)
from rest_framework.response import Response
from rest_framework.request import Request
from cloudinary import CloudinaryImage
from .permissions import SoloAdminPuedeEscribir, SoloMozoPuedeEscribir
from fact_electr.models import Pedido, DetallePedido
from rest_framework import status
from django.utils import timezone


class PlatoApiView(ListCreateAPIView):
    serializer_class=PlatoSerializer
    queryset=Plato.objects.all()
    # tipos de permisos que el cliente necestia para realizar la peticion
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get(self, request:Request):        
        data=self.serializer_class(instance=self.get_queryset(), many=True)
        # hacer una iteracion para modificar la foto de cada plato y devolver el link de la foto
        print(data.data[1].get('foto'))
        # del contenido de la foto solamente extraer el nombre del archivo o si esten en uan carpeta extraer la carpeta y archivo
        link=CloudinaryImage(
            'plato/xoo5lqjgt3z4whvmb9st.jpg').image(secure=True)

        print(link)
        return Response(data=data.data)
        
class StockApiView(ListCreateAPIView):
    serializer_class=StockSerializer
    queryset= Stock.objects.all()
    permission_classes=[IsAuthenticated, SoloAdminPuedeEscribir]

class PedidoApiView(ListCreateAPIView):
    queryset=Pedido.objects.all()
    serializer_class=PedidosSerializer
    permission_classes=[IsAuthenticated, SoloMozoPuedeEscribir]

    def post(self, request:Request):
        print(request.user)
        # le agrego al body el usuarioId proveniente de la token
        request.data['usuarioId']=request.user.id
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()

        return Response(data=data.data, status=status.HTTP_201_CREATED)

class AgregarDetallePedidoApiView(CreateAPIView):
    queryset=DetallePedido.objects.all()
    serializer_class=AgregarDetallePedidoSerializer

    def post(self, request:Request):
        # 1. valido la data con el serializer
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        # 2. verifico que tenga esa cantidad de productos en stock
        stock=Stock.objects.filter(fecha=timezone.now(),
                                    platoId=data.validated_data.get('platoId')).first()
        print(stock)
        if stock is None:
            return Response (data={'message':'No hay stock para ese producto para el dia de hoy'},
                            status=status.HTTP_400_BAD_REQUEST)
        # información que me envía el front
        #{
        # "cantidad":2,
        # "plato":1,
        # "pedido_id": 2
        # }
        # verificar que en el stock esté en base al dia de hoy esa cantidad
        # 3. agrego el detalle
        return Response(data={'message':'Detalle agregado exitosamente'})