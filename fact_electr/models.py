from django.db import models
from autorizacion.models import Usuario
from menu.models import Stock

class Pedido(models.Model):
    id=models.AutoField(primary_key=True)
    fecha=models.DateTimeField()
    total=models.FloatField(null=False)
    numeroDocumentoCliente=models.CharField(max_length=12)
    tipoDocumentoCliente=models.CharField(
        choices=(['RUC', 'RUC'], ['DNI','DNI']), max_length=5)
    mesa=models.ImageField()
    propina= models.FloatField()

    usuarioId=models.ForeignKey(
        to =Usuario, related_name='pedidos', db_column='usuario_id', on_delete=models.CASCADE)
    class Meta:
        db_table='pedidos'



class Comprobante(models.Model):
    id=models.AutoField(primary_key=True)
    serie=models.CharField(max_length=5, null=False)
    numero=models.CharField(max_length=10, null=False)
    pdf=models.TextField()
    cdr= models.TextField()
    xml=models.TextField()
    tipo=models.CharField(choices=(['BOLETA', 'BOLETA'],['FACTURA','FACTURA']), null=False, max_length=10)

  

    pedido= models.OneToOneField(
        to=Pedido, related_name='comprobante', on_delete=models.CASCADE, db_column='pedido_id')

    class Meta:
        db_table='comprobantes'
        unique_together=[['serie','numero']]

class DetallePedido(models.Model):
    id=models.AutoField(primary_key=True)
    cantidad=models.IntegerField()
    stockID=models.ForeignKey(
        to=Stock, related_name='pedidos', on_delete=models.CASCADE, db_column='stock_id')
    pedidoId= models.ForeignKey(
            to =Pedido, related_name='detalle_pedidos', on_delete=models.CASCADE, db_column='pedido_id')

    class Meta:
            db_table= 'detalle_pedidos'