from datetime import datetime
import requests
from menu.models import Plato, Stock
from .models import Comprobante, Pedido, DetallePedido
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
    ultimoComprobante=Comprobante.objects.values_list('numero','serie').filter(
        tipo=tipo).order_by('-numero').first()

    if ultimoComprobante is None:
        numero=1
    else:
        numero=int(ultimoComprobante[0]) + 1
    
    if tipo_documento is None:
        cliente_tipo_de_documento='-'
        cliente_numero_de_documento =None

    else:
        if tipo_documento=='RUC':
            cliente_tipo_de_documento=6
        elif tipo_documento=='DNI':
            cliente_tipo_de_documento=1

        cliente_numero_de_documento= numero_documento

        if tipo_documento == 'RUC':
            respuesta_apiperu=requests.get("https://apiperu.dev/api/ruc/"+numero_documento,
                        headers={'Authorization':'Bearer '+environ.get('APIPERU_TOKEN')})

            if respuesta_apiperu.json().get('succes')== False:
                raise Exception ('Datos del cliente no válidos')
            else:
                cliente_denominacion=respuesta_apiperu.json().get(
                    'data').get('nombre_o_razon_social')
                cliente_direccion=respuesta_apiperu.json().get('data').get('direccion_completa')
        
        elif tipo_documento =='DNI':
            respuesta_apiperu=requests.get("https://apiperu.dev/api/dni/"+numero_documento,
                        headers={'Authorization':'Bearer '+environ.get('APIPERU_TOKEN')})  

            if respuesta_apiperu.json().get('success')==False:
                raise Exception('Datos del cliente no válidos')                        
            else:
                cliente_denominacion=respuesta_apiperu.json('data').get('nombre_completo')
                cliente_direccion=''
        cliente_email='rbeltrann@gmail.com'

    fecha_de_emision=datetime.now().strftime('%d-%m-%Y')
    moneda=1
    porcentaje_de_igv=18.00

    #valor total de la venta (INC IGV)
    total=float(pedido.total)

    # el valor sin el igv (la base imponible)
    total_gravada=pedido.total/1.18
    # https://boletin.luacontadores.com/2020/08/como-calcular-el-igv-calculadora-igv.html#:~:text=IGV%202020%20%2D%20Per%C3%BA-,El%20c%C3%A1lculo%20de%20IGV%20se%20hace%20aplicando%20el%2018%25%20en,de%20saber%20el%20i...
    # el valor del igv de la venta
    total_igv=total-total_gravada
    enviar_automaticamente_a_la_sunat = True
    enviar_automaticamente_al_cliente = True
    formato_de_pdf='TICKET' # A4' # A5 | TICKET

    detalle_pedido:list[DetallePedido]=pedido.detalle_pedidos.all()

    detraccion=False
    items=[]
    for detalle in detalle_pedido:
        #extraigo el stock de ese detalle
        stock:Stock=detalle.stockId
        # extraigo el plato de ese stock
        plato:Plato=stock.platoId

        undidad_de_medida='NIU'
        codigo=plato.id
        descripcion=plato.nombre
        cantidad=detalle.cantidad
        # el precio del plato con igv
        precio_unitario=float(stock.precio_diario)
        #el precio del plato sin igv
        valor_unitario=precio_unitario/1.18

        subtotal=valor_unitario*cantidad
        tipo_de_igv=1
        igv=subtotal*0.18
        total_producto=precio_unitario*cantidad

        item = {
            'unidad_de_medida':undidad_de_medida,
            'codigo': codigo,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'valor_unitario': valor_unitario,
            'precio_unitario':precio_unitario,
            'subtotal': subtotal,
            'tipo_de_igv': tipo_de_igv,
            'igv': igv,
            'total': total_producto,
            'anticipo_regularizacion': False
        }

        items.append(item)

    comprobante_body = {
        'operacion': operacion,
        'tipo_de_comprobante': tipo_de_comprobante,
        'serie': serie,
        'numero': numero,
        'sunat_trasaction': sunat_transaction,
        'cliente_tipo_de_documento': cliente_tipo_de_documento,
        'cliente_numero_de_documento': cliente_numero_de_documento,
        'cliente_denominacion': cliente_denominacion,
        'cliente_direccion': cliente_direccion,
        'cliente_email': cliente_email,
        'fecha_de_emision': fecha_de_emision,
        'moneda': moneda,
        'porcentaje_de_igv': porcentaje_de_igv,
        'total_gravada': total_gravada,
        'total_igv': total_igv,
        'total': total,
        'detraccion': detraccion,
        'observaciones': '',
        'enviar_automaticamente_a_la_sunat':enviar_automaticamente_a_la_sunat,
        'enviar_automaticamente_al_cliente':enviar_automaticamente_al_cliente,
        'medio_de_pago': 'EFECTIVO',
        'formato_de_pdf': formato_de_pdf,
        'items':items
        }
    url_nubefact=environ.get('NUBEFACT_URL')
    headers_nubefact={
        'Authorization':environ.get('NUBEFACT_TOKEN'),
        'Content-Type':'application/json'
    }
    respuestaNubefact=requests.post(
        url_nubefact, headers=headers_nubefact, json=comprobante_body)
    
    print(respuestaNubefact.json())




    
