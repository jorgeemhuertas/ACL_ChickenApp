from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('visitante', 'Visitante'),
    ]
    nombre = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Hash
    rol = models.CharField(max_length=10, choices=ROLES)

    def nivel(self):
        return {'visitante': 1, 'empleado': 2, 'admin': 3}[self.rol]

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Archivo(models.Model):
    CATEGORIAS = [
        ('publico', 'Público'),
        ('confidencial', 'Confidencial'),
        ('topsecret', 'Top Secret'),
    ]
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=15, choices=CATEGORIAS)

    def nivel(self):
        try:
            return {'publico': 1, 'confidencial': 2, 'topsecret': 3}[self.categoria]
        except KeyError:
            print(f"KeyError: categoria value is '{self.categoria}'")
            # Default to the lowest level as a fallback
            return 1

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

class ACL(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    puede_leer = models.BooleanField(default=False)
    puede_escribir = models.BooleanField(default=False)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)



