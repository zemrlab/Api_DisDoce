from django.db import models
from apps.usuario.models import Usuario
# Create your models here.

class Docente(models.Model):
    id_usuario = models.ForeignKey(Usuario, db_column='id_usuario',on_delete=models.CASCADE, blank=True, null=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apell_pat = models.CharField(max_length=100, blank=True, null=True)
    apell_mat = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=30, blank=True, null=True)
    tipo_document = models.CharField(max_length=100, blank=True, null=True)
    nro_document = models.CharField(max_length=100, blank=True, null=True)
    codigo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    celular = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100)
    linkedinid = models.CharField(db_column='linkedInId', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    genero = models.CharField(max_length=1, blank=True, null=True)
    pag_web = models.CharField(max_length=100, blank=True, null=True)
    foto = models.CharField(max_length=100, blank=True, null=True)
    fecha_nac = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    mayor_grado = models.CharField(max_length=100, blank=True, null=True)
    menc_grado = models.CharField(max_length=100, blank=True, null=True)
    universidad = models.CharField(max_length=100, blank=True, null=True)
    pais_grado = models.CharField(max_length=100, blank=True, null=True)
    cv = models.CharField(max_length=100, blank=True, null=True)
    fech_ingreso = models.CharField(max_length=100, blank=True, null=True)
    sunedu_ley = models.CharField(max_length=2, blank=True, null=True)
    nivel_programa = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    regimen_dedicacion = models.CharField(max_length=100, blank=True, null=True)
    horas_semanales = models.CharField(max_length=100, blank=True, null=True)
    investigador = models.CharField(max_length=2, blank=True, null=True)
    dina = models.CharField(max_length=2, blank=True, null=True)
    per_academico = models.CharField(max_length=100, blank=True, null=True)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    resetpasswordexpires = models.DateTimeField(db_column='resetPasswordExpires', blank=True, null=True)  # Field name made lowercase.
    resetpasswordtoken = models.CharField(db_column='resetPasswordToken', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    logins = models.IntegerField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)  # This field type is a guess.
    tokens = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'docente'

class TipoGrado(models.Model):
    id_tip_grado = models.CharField(primary_key=True, max_length=2)
    nom_tip_grado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_grado'
class DatosAcademicos(models.Model):
    id_dat_academicos = models.IntegerField(primary_key=True)
    id_docente = models.ForeignKey(Docente, db_column='id_docente',on_delete=models.CASCADE)
    id_tip_grado = models.ForeignKey(TipoGrado, db_column='id_tip_grado',on_delete=models.CASCADE)
    mencion_grado = models.CharField(max_length=60)
    centro_estudios = models.CharField(max_length=60)
    pais_estudios = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'datos_academicos'