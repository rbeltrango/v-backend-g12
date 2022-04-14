from rest_framework import serializers
from .models import Usuario

class RegistroUsuarioSerializer(serializers.ModelSerializer):

    def save(self):
        # creando una isntancia de mi usuario con los campos ya validados (validaded_data)
        nuevoUsuario=Usuario(**self.validated_data)
        nuevoUsuario.set_password(self.validated_data.get('password'))
        nuevoUsuario.save()

    class Meta:
        model = Usuario
        exclude=['groups','user_permissions']
        # fields='__all__'
        # mediante el atributo extra_kewargs indicar que la password será de sólo escritura y además que el id sea sólo lectura
        extra_kwargs= {
            'password':{
                'write_only':True

            },
            'id':{
                'read_only':True
            }
        }

