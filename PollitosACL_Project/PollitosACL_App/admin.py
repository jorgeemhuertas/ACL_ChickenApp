from django.contrib import admin
from .models import Usuario, Archivo, ACL

admin.site.register(Archivo)
admin.site.register(Usuario)
