from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """ Clase que sirve para manejar el comprtamemiento del auth_user """
    def create_user(self, correo, nombre, rol, password):
        """ creacion de un usuario sin el comando createsuperuser """
        if not correo:
            raise ValueError('el usuario ddebe tener obligatoriamente un correo')

        # normalize el correo  aparte de validar que sea un correo válido removerá los 
        #espacios innecesarios
        correo=self.normalize_email(correo)
        # llama al usuario e iniciará su construcción
        nuevoUsuario=self. model(correo=correo, nombre=nombre, rol=rol)
        # set_password generará un hash de la contraseña usando bcrypt y el algoritmo SHA256
        nuevoUsuario.set_password(password)
        # sirve para referenciar a la base de datos x default en el caso que tengamos varias 
        # conexiones a diferentes bases de datos
        nuevoUsuario.save(using=self._db)
        return nuevoUsuario
    
    def create_superuser(self, correo, nombre, rol, password):
        """ creación de un super por consola, este método se mandará a llamar cuanod se haga 
        uso del comando por consola """
        usuario=self.create_user(correo, nombre, rol, password)
        # is_superuser indicará que usuarios son superusuarios y podrá acceder a todas las 
        # funcionalidades del panel administrativo
        usuario.is_superuser=True
        usuario.is_staff=True

        usuario.save(using=self._db)
