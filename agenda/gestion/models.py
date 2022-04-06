from django.db import models

class Etiqueta(models.Model):
    # Tipos de Columnas > https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-types
    # Opciones de las columnas > https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-options
    id=models.AutoField(primary_key=True, unique=True, null=False)
    nombre= models.CharField(max_length=20, unique=True, null=False)
    # Columnas de auditoria
    # son columnas que podran ayudar al seguimiento de la creacion de registros
    # createdAt > es la fecha en la cual se creo el registro
    createdAt=models.DateTimeField(auto_now_add=True, db_column='created_at')
    # updatedAt > es la fecha en la cual se modifico algun campo del registro
    updatedAt=models.DateTimeField(auto_now=True, db_column='updated_at')

    # todas las configuraciones propias de la tabla se haran mediante la definicion de sus atributos en la clase Meta
    # https://docs.djangoproject.com/en/4.0/ref/models/options/
    class Meta:
        # cambiar el nombre de la tabla en la bd (a diferencia del nombre de la clase)
        db_table='etiquetas'
        # modficando el ordenameinto ascendeten se le pone menos ('-nombre')para que sea descendente
        ordering=['-nombre']


class Tareas(models.Model):

    class CategoriaOpciones(models.TextChoices):
    # CADA opcion le podemos colocar dos parametros. El primero será una abreviatura para que se guarde en la BD y el segundo el nombre completo
        TODO='TODO', 'TO_DO'
        IN_PROGRESS='IP', 'IN_PROGRESS'
        DONE='DONE','DONE'
        CANCELLED='CANCELLED', 'CANCELLED'

    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=45, null=False)
    # Forma 1 usando una subclase que herede de TextChoices
    categoria=models.CharField(max_length=45, choices=CategoriaOpciones.choices,default=CategoriaOpciones.TODO)
    # Forma 2 usando una lista de tuplas
    # categoria = models.CharField(max_length=45, choices=[
    #     ('TODO','TO_DO'), 
    #     ('IP', 'IN_PROGRESS'),
    #     ('DONE', 'DONE'),
    #     ('CANCELLED', 'CANCELLED')
    #     ], default='TODO')

    fechaCaducidad=models.DateTimeField(db_column='fecha_caducidad')
    importancia=models.IntegerField(null=False)
    descripcion=models.TextField()
    
    createdAt=models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt=models.DateTimeField(auto_now=True, db_column='updated_at')

    # vamos a crear una relacion de muchos a muchos
    # en Django se puede realizar las relaciones one-to-one, one-to-many o many-to-many
    # para crear las relaciones entre tablas, acá ya no es necesario crear las relationships
    # porque ya están integradas dentro de la relacion
    etiquetas=models.ManyToManyField(to=Etiqueta, related_name='tareas')

    class Meta:
        db_table='tareas'

# Si la tabla tareas_etiquetas no fuese una tabla pivote, detalle entonces tendría que crer la tabla como si fuera una tabla común
# class TareasEtiquetas(models.Model):
#     ...
#     etiquetaFK = models.ForeignKey(to=Etiqueta)
#     tareaFK = models.ForeignKey(to=Tareas)
#     # las demas columnas
       