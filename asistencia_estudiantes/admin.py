from django.contrib import admin
from .models import Estudiante, Clase, RegistroAsistencia, CaracteristicasFaciales

admin.site.register(Estudiante)
admin.site.register(Clase)
admin.site.register(RegistroAsistencia)
admin.site.register(CaracteristicasFaciales)
