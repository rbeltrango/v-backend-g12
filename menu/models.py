from django.db import models
from cloudinary import models as modelsCloudinary
from django.forms import FloatField

# Create your models here.
class Plato(models.Model):
    id= models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=45, null=False)
    foto=modelsCloudinary.CloudinaryField(
        folder='plato') # models.ImageFiled()
    

    disponible=models.BooleanField(default=True, null=False)
    precio=models.FloatField(null=False)

    class Meta:
        db_table='platos'

class Stock(models.Model):
    id= models.AutoField(primary_key=True)
    fecha=models.DateField(null=False)
    cantidad=models.IntegerField(null=False)
    precio_unitario=models.FloatField(null=False)

    # related_name > servirá para ingresar desde el modelo del cual se está creando la relación (en este caso desde
    # platos podremos ingresar a todos los stocks)
    # on_delete > qué accción tomará cuando se desea eliminar el padre (la PK)
    # CASCADE > eliminará el registro del plato y todos  los stocks que tengan ese registro también serán eliminados en cascada
    # PROTECT > impedirá que se realice la eliminación del plato si se tiene stocks
    # SET NULL > eliminará el plato y todos sus stocks colocará en su FK el valor de NULL
    # DO_NOTHING >  elimará el plato y no cambiará nada de los stocks (seguirán con el mismo valor ya eliminado)
    # RESTRICT > no permite la eliminación y lanzarjá un error de tipo RestrictedError (hará un raise)
    #  https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    platoId=models.ForeignKey(
        to=Plato, related_name='stocks', on_delete=models.CASCADE, db_column='plato_id')

    class Meta:
        db_table='stocks'
        # unique_together > crea un índice de dos o más columnas en el cual no se podrán repetir los mismos valores de esas columnas
        # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey.on_delete
        # fecha     |   plato_id
        # 2022-04-18|   1   error
        # 2022-04-18|   1   error
        # 2022-04-18|   2   ok
        # 2022-04-19|   1   ok


        unique_together=[['fecha','platoId']]

