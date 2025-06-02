from django.db import models

# Create your models here.
class Institucion(models.Model):
    id_institucion = models.AutoField(primary_key=True)
    rut_institucion = models.CharField(max_length=12, unique=True)
    nombre_institucion = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=50, null=False, blank=False)
    sitio_web = models.CharField(max_length=50, null=True, blank=True)
    representante_legal = models.CharField(max_length=50, null=False, blank=False)
    telefono_institucion = models.CharField(max_length=12, null=False, blank=False)
    correo_institucion = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.nombre_institucion

class Profesor(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    id_profesor = models.AutoField(primary_key=True)
    rut_profesor = models.CharField(max_length=12, unique=True)
    nombre_profesor = models.CharField(max_length=50, null=False, blank=False)
    apellido_profesor = models.CharField(max_length=50, null=False, blank=False)
    correo_profesor = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=False, blank=False)
    altura = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    antecedentes_medicos = models.CharField(max_length=100, null=True, blank=True)
    area_docencia = models.CharField(max_length=50, null=False, blank=False)
    id_institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)

    def __str__(self):
        return self.rut_profesor
    
class Aula(models.Model):
    id_aula = models.AutoField(primary_key=True)
    nro_aula = models.CharField(max_length=10, null=False, blank=False) 
    tamaño = models.IntegerField(null=True, blank=True)
    cantidad_alumnos = models.IntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    id_institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
   
    class Meta:
        unique_together = ('nro_aula', 'id_institucion')  # 🔹 Restricción de unicidad
   
    def __str__(self):
        return self.nro_aula

class Horario(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    id_horario = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA, null=False, blank=False)
    hora_inicio = models.TimeField(null=False, blank=False)
    hora_termino = models.TimeField(null=False, blank=False)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    id_aula = models.ForeignKey(Aula, on_delete=models.CASCADE)

    def __str__(self):
        return self.dia

class Dispositivo_IoT(models.Model): 
    TIPO_CHOICES = [
        ('1', 'Dosímetro de Voz'),
        ('2', 'Registrador de Variables Ambientales'),
    ]
    id_dispositivo = models.AutoField(primary_key=True)
    mac_dispositivo = models.CharField(max_length=17, unique=True)
    tipo_dispositivo = models.CharField(max_length=1, choices=TIPO_CHOICES, null=False, blank=False)
    activo = models.BooleanField(default=False)  # 🔹 Campo para indicar si el dispositivo está activo

    def __str__(self):
        return self.mac_dispositivo

class Dispositivo_IoT_Aula(models.Model):
    id_dispositivo_aula = models.AutoField(primary_key=True)
    id_dispositivo = models.ForeignKey(Dispositivo_IoT, on_delete=models.CASCADE)
    id_aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    

    class Meta:
        unique_together = ('id_dispositivo', 'id_aula')  # 🔹 Restricción de unicidad

    def __str__(self):
        return f"{self.id_dispositivo} - {self.id_aula}"


# relacion entre Dispositivo_IoT y profesor
class Dispositivo_IoT_Profesor(models.Model):
    id_dispositivo_profesor = models.AutoField(primary_key=True)
    id_dispositivo = models.ForeignKey(Dispositivo_IoT, on_delete=models.CASCADE)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_dispositivo', 'id_profesor')  # 🔹 Restricción de unicidad

    def __str__(self):
        return f"{self.id_dispositivo} - {self.id_profesor}"