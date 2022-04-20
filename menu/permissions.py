from ast import Return
from urllib import request
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

# https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
class SoloAdminPuedeEscribir(BasePermission):
    message='Este usuario no tiene permisos'

    def has_permission(self, request: Request, view):
        # el request nos dará toda la información del los atributos de la petición
        # siempre retornar TRUE OR FALSE para indicar si cumple o no los permisos determinados
        print(request.user)
        print(request.user.nombre)
        print(request.user.rol)
        # auth > imprimirá la token de la atutenticación que se usa para esta solicitud (request)
        print(request.auth)

        print (request.method)

        print(SAFE_METHODS)
        print(type(view))

        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.rol=='ADMINISTRADOR'

        # return True if request.method in SAFE_METHODS else request.user.rol=='ADMINISTRADOR'

class SoloMozoPuedeEscribir(BasePermission):
    def has_permission(self, request:Request, view):
        if request.method==SAFE_METHODS:
            return True
        else:
            return request.user.rol=='MOZO'