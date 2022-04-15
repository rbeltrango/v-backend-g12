from .models import Plato
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from .serializer import PlatoSerializer
from rest_framework.permissions import (
AllowAny, # sirve para que el controlador se pubilco
IsAuthenticated, # los controladores soliciten una token de acceso
IsAuthenticatedOrReadOnly, # sólo para los métodos get no será necesario la token pero para (POST, PUT,DELETE,PATCH SÍ será requerido)
IsAdminUser, # verifica que en la token de acceso buscará al usuario y verá si es superuser (is_superuser)
)
from rest_framework.response import Response
from rest_framework.request import Request
from cloudinary import CloudinaryImage

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
        