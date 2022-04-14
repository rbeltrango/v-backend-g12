from django.db import models
# AbstractBaseUser permite modificar todo el modelo auth_user desde cero

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .authManager import UserManager

# Create your models here.
class Usuario(AbstractBaseUser, PermissionsMixin):
    id=models.AutoField(primary_key=True)
    correo=models.EmailField(unique=True, null=False)
    password=models.TextField(null=False)
    nombre=models.CharField(max_length=45, null=False)
    rol=models.CharField(choices=(
        # con la cual se usará en al bd y se mostrará la que se usará para los formularios
        ['ADMINISTRADOR', 'ADMINISTRADOR'],
        ['MOZO','MOZO']), max_length=40)

    is_staff =models.BooleanField(default=True)
    # is_active puede realizar  operaciones dentro del panel administrativo, si el usuario
    # no esta activo podrá logearse pero no podrá realizar ninguna acción
    is_active=models.BooleanField(default=True)

    createdAt=models.DateTimeField(auto_now_add=True, db_column='created_at')
    
    # comportamiento que tendrá el modelo cuando se realice el comando createsuperuser 
    objects=UserManager()

    # será el campo que pedirá 
    USERNAME_FIELD='correo'

    # serán los atributos que se solicitaran por la consola al crear el superussuario
    REQUIRED_FIELDS=['nombre', 'rol']

    class Meta:
        db_table='usuarios'



