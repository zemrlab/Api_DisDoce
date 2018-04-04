# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
"""from django.db import models


class Accede(models.Model):
    id_tu = models.ForeignKey(TipoUsuario, models.DO_NOTHING, db_column='id_tu', primary_key=True)
    id_mod = models.ForeignKey('Modulo', models.DO_NOTHING, db_column='id_mod')

    class Meta:
        managed = False
        db_table = 'accede'
        unique_together = (('id_tu', 'id_mod'),)
class Administrativo(models.Model):
    id_admin = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    codigo = models.DecimalField(unique=True, max_digits=65535, decimal_places=65535)
    dni = models.DecimalField(unique=True, max_digits=65535, decimal_places=65535)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'administrativo'
class Alumno(models.Model):
    id_alum = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    nom_ape = models.CharField(max_length=70)
    codigo = models.DecimalField(unique=True, max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'alumno'
class Directiva(models.Model):
    id_direc = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    codigo = models.DecimalField(unique=True, max_digits=65535, decimal_places=65535)
    dni = models.DecimalField(unique=True, max_digits=65535, decimal_places=65535)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'directiva'

class ExperienciaAsesorDocente(models.Model):
    id_exp_asesor_docente = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='id_docente')
    universidad = models.CharField(max_length=80)
    tesis = models.CharField(max_length=70)
    tesista = models.CharField(max_length=70)
    repositorio = models.CharField(max_length=70)
    fecha_aceptacion = models.DateField(blank=True, null=True)
    createdat = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiencia_asesor_docente'
class ExperienciaLaboral(models.Model):
    id_exp_laboral = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='id_docente')
    empresa = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    createdat = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiencia_laboral'
class LaboralDocente(models.Model):
    id_laboral_doc = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='id_docente')
    universidad = models.CharField(max_length=80)
    tipo_docente = models.CharField(max_length=50)
    fecha_inicio = models.DateField(blank=True, null=True)
    createdat = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'laboral_docente'
class Modulo(models.Model):
    id_mod = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    nombre = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'modulo'
class NivelesPrograma(models.Model):
    id_niveles_program = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='id_docente')
    pregrado = models.CharField(max_length=2)
    maestria = models.CharField(max_length=2)
    doctorado = models.CharField(max_length=2)
    createdat = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'niveles_programa'
class ProyectoInvestigacion(models.Model):
    id_proyecto_invest = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='id_docente')
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    area_ocde = models.CharField(max_length=50)
    createdat = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proyecto_investigacion'
class Recaudaciones(models.Model):
    id_rec = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_alum = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alum')
    moneda = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dependencia = models.CharField(max_length=50, blank=True, null=True)
    concep = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    concep_a = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    concep_b = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    numero = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    codigo = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    nombres = models.CharField(max_length=70, blank=True, null=True)
    importe = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    carnet = models.CharField(max_length=30, blank=True, null=True)
    autoseguro = models.CharField(max_length=30, blank=True, null=True)
    ave = models.CharField(max_length=30, blank=True, null=True)
    devol_tran = models.CharField(max_length=30, blank=True, null=True)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.CharField(max_length=50, blank=True, null=True)
    flag_pago = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'recaudaciones'
"""