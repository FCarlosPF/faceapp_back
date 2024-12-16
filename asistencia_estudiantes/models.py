from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    numero_matricula = models.CharField(max_length=50, unique=True)
    foto = models.ImageField(upload_to='fotos_estudiantes/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'estudiantes'  # Define el esquema y tabla
        managed = False
    


class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'clases'  # Define el esquema y tabla
        managed = False

class RegistroAsistencia(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tarde', 'Tarde'),
    ])
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.fecha}"

    class Meta:
        db_table = 'registros_asistencia'  # Define el esquema y tabla
        managed = False


class CaracteristicasFaciales(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
    vector_caracteristicas = models.JSONField()  # Almacena el vector en formato JSON
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Características faciales de {self.estudiante}"

    class Meta:
        db_table = 'caracteristicas_faciales'  # Define el esquema y tabla
        managed = False