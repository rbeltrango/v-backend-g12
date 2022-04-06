from django.db import models

class Etiqueta(models.Model):
    id=models.AutoField(primary_key=True, unique=True, null=False)
    nombre= models.CharField(max_length=20, unique=True, null=False)
    # columnas de auditoria
    # ayuudan a lseugiemito de creacion de registros
    createdAt=models.DateTimeField(auto_now_add=True, db_column='created_at')

    updatedAt=models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table='etiquetas'
        # modficando el ordenameinto ascendeten se le pone menos ('-nombre')para que sea descendente
        ordering=['-nombre']

class Tareas(models.Model):

    # CADA opcion le podemos colocar dos parametros. El primero será una abreviatura para que se guarde en la BD y el segundo el nombre completo
    class CategoriaOpciones(models.TextChoices):
        TODO='TODO', 'TO_DO'
        IN_PROGRESS='IP', 'IN_PROGRESS'
        DONE='DONE','DONE'
        CANCELLED='CANCELLED', 'CANCELLED'

    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=45, null=False)
    categoria=models.CharField(max_length=45, choices=CategoriaOpciones.choices,default=CategoriaOpciones.TODO)

    fechaCaducidad=models.DateTimeField(db_column='fecha_caducidad')
    importancia=models.IntegerField(null=False)

    createdAt=models.DateTimeField(auto_now_add=True, db_column='created_at')
    updatedAt=models.DateTimeField(auto_now=True, db_column='updated_at')

# vamos a crear una relacion de muchos a muchos
# en Django se puede realizar las relaciones one-to-one, one-to-many o many-to-many
# para crear las relaciones entre tablas, acá ya no es necesario crear las relationships
# porque ya están integradas dentro de la relacion
    etiquetas=models.ManyToManyField(to=Etiqueta, related_name='tareas')

    class Meta:
        db_table='tareas'
       