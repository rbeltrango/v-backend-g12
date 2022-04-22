import requests
from .models import Comprobante, Pedido
from django.db import connection
from os import environ


def generar_comprobante(tipo_de_comprobante:int, tipo_documento:str, numero_documento:str, pedido_id:int):
    # sirve para generar un comprobante electronico ya sea factura  , boleta etc en base a un pedido
    pedido=Pedido.objects.filter(id=pedido_id).first()
    if pedido is None:
        raise Exception('Pedido no existe')
    if pedido.total > 700 and tipo_documento is None:
            raise Exception('El pedido al ser mayor a 700 soles tiene que tener un cliente registrado')

    operacion='generar_comprobante'
    tipo=''
    sunat_transaction=1
    if tipo_de_comprobante==1:
        # esta serie se debería guardar en la bd en una tabla de series para que cuando el contador desee cambiar de serie se m
        #ifique en esa tabla
        serie='FFF1'
        tipo='FACTURA'

    elif tipo_de_comprobante==2:
        serie='BBB1'
        tipo='BOLETA'

    elif tipo_de_comprobante==3 or tipo_de_comprobante==4:
        serie='0001'
        tipo='NOTA'

    # el número lo sacaremos del último comprobante almacenado en la base de datos
    # si queremos hacer uso de una vista, vista materializada funcion o procedimiento alamcenado que no esté registrado en el ORM
    # entonces podremos hacer uso de  na RAW QUERY de la siguiente manera:
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM vista_prueba')
        print(cursor.fetchall())


    # lo sacaremos del ultimo comprobante alamcenado en la base de datos
    # SELECT * FROM comprobantes WHERE tipo = 'boleta' | 'factura' ORDER BY numero desc LIMIT 1;
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#order-by
    ultimoComprobante=Comprobante.objetcs.values_list('numero','serie').filter(
        tipo=tipo).order_by('-numero').first()

    if ultimoComprobante is None:
        numero=1
    else:
        numero=int(ultimoComprobante[0]) + 1
    
    if tipo_documento is None:
        cliente_tipo_de_documento='-'
        cliente_numero_de_documento =None

    else:
        cliente_tipo_de_documento=tipo_documento
        cliente_numero_de_documento= numero_documento

        if tipo_documento == 'RUC':
            respuesta_apiperu=requests.get("https://apiperu.dev/api/ruc/"+numero_documento,
                        headers={'Authorization':'Bearer'+environ.get('APIPERU_TOKEN')})

            if respuesta_apiperu.json().get('succes')== False:
                raise Exception ('Datos del cliente no válidos')
            else:
                cliente_denominacion=respuesta_apiperu.json().get(
                    'data').get('nombre_o_razon_social')
        
        elif tipo_documento =='DNI':
            respuesta_apiperu=requests.get("https://apiperu.dev/api/dni/"+numero_documento,
                        headers={'Authorization':'Bearer'+environ.get('APIPERU_TOKEN')})  
            if respuesta_apiperu.json().get('success')==False:
                raise Exception('Datos del cliente no válidos')                        
            else:
                cliente_denominacion=respuesta_apiperu.json('data').get('nombre_completo')


    
