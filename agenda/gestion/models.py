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
        ordering=['nombre'] 

        

