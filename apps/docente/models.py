from django.db import models
from apps.usuario.models import Usuario
# Create your models here.

class Docente(models.Model):
    id_docente = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, db_column='id_usuario',on_delete=models.CASCADE)
    nom_docente = models.CharField(max_length=50)
    ape_docente = models.CharField(max_length=50)
    codigo_docente = models.CharField(max_length=10)
    dni_docente = models.CharField(max_length=8)
    email_docente = models.CharField(max_length=70)
    celular_docente = models.CharField(max_length=9)
    genero = models.CharField(max_length=1)
    pagina_web = models.CharField(max_length=50)
    #foto = models.BinaryField()
    fecha_nac = models.DateField()
    pais = models.CharField(max_length=50)
    direccion = models.CharField(max_length=80)
    sunedu_le = models.CharField(max_length=2)
    categoria = models.CharField(max_length=30)
    regimen_dedicacion = models.CharField(max_length=30)
    cv = models.CharField(max_length=100)

    class Meta:
        #managed = False
        db_table = 'docente'

class TipoGrado(models.Model):
    id_tip_grado = models.CharField(primary_key=True, max_length=2)
    nom_tip_grado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'tipo_grado'
class DatosAcademicos(models.Model):
    id_dat_academicos = models.IntegerField(primary_key=True)
    id_docente = models.ForeignKey(Docente, db_column='id_docente',on_delete=models.CASCADE)
    id_tip_grado = models.ForeignKey(TipoGrado, db_column='id_tip_grado',on_delete=models.CASCADE)
    mencion_grado = models.CharField(max_length=60)
    centro_estudios = models.CharField(max_length=60)
    pais_estudios = models.CharField(max_length=50)

    class Meta:
        #managed = False
        db_table = 'datos_academicos'