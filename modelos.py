# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accede(models.Model):
    id_mod = models.ForeignKey('Modulo', models.DO_NOTHING, db_column='id_mod', primary_key=True)
    id_perfil = models.ForeignKey('Perfil', models.DO_NOTHING, db_column='id_perfil')

    class Meta:
        managed = False
        db_table = 'accede'
        unique_together = (('id_mod', 'id_perfil'),)


class AdministadorSistemas(models.Model):
    id_adm_sis = models.SmallIntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    nomb_adm_sis = models.CharField(max_length=50)
    ape_adm_sis = models.CharField(max_length=50)
    codigo_adm_sis = models.CharField(unique=True, max_length=8, blank=True, null=True)
    dni_adm_sis = models.CharField(unique=True, max_length=8)
    email_adm_sis = models.CharField(max_length=50)
    telefono_adm_sis = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'administador_sistemas'


class Administrativo(models.Model):
    id_admin = models.SmallIntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    codigo = models.CharField(unique=True, max_length=8)
    dni = models.CharField(unique=True, max_length=8)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'administrativo'


class Alumno(models.Model):
    id_alum = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_facultad = models.ForeignKey('Facultad', models.DO_NOTHING, db_column='id_facultad')
    ape_nom = models.CharField(unique=True, max_length=300)
    codigo = models.CharField(max_length=15, blank=True, null=True)
    dni = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alumno'


class AlumnoPrograma(models.Model):
    cod_alumno = models.CharField(primary_key=True, max_length=8)
    dni_m = models.ForeignKey('MAlumno', models.DO_NOTHING, db_column='dni_m', blank=True, null=True)
    id_programa = models.ForeignKey('Programa', models.DO_NOTHING, db_column='id_programa')
    ape_paterno = models.CharField(max_length=60)
    ape_materno = models.CharField(max_length=60, blank=True, null=True)
    nom_alumno = models.CharField(max_length=100)
    cod_especialidad = models.CharField(max_length=4, blank=True, null=True)
    cod_tip_ingreso = models.CharField(max_length=4, blank=True, null=True)
    cod_situ = models.CharField(max_length=4, blank=True, null=True)
    cod_perm = models.CharField(max_length=4, blank=True, null=True)
    anio_ingreso = models.CharField(max_length=30, blank=True, null=True)
    des_especialidad = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alumno_programa'
        unique_together = (('cod_alumno', 'id_programa'),)


class Auditoria(models.Model):
    id_admin = models.ForeignKey(Administrativo, models.DO_NOTHING, db_column='id_admin', primary_key=True)
    id_rec = models.ForeignKey('Recaudaciones', models.DO_NOTHING, db_column='id_rec')
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'auditoria'
        unique_together = (('id_admin', 'id_rec'),)


class CfgRecaudacionesDet(models.Model):
    cfg_recdet_id = models.IntegerField(primary_key=True)
    cfg_recdet_estado = models.CharField(max_length=1, blank=True, null=True)
    cfg_recdet_valor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cfg_recaudaciones_det'


class Ciclo(models.Model):
    id_ciclo = models.AutoField(primary_key=True)
    nom_ciclo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ciclo'


class ClasePagos(models.Model):
    id_clase_pagos = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clase_pagos'


class Concepto(models.Model):
    id_concepto = models.SmallIntegerField(primary_key=True)
    concepto = models.CharField(unique=True, max_length=6)
    concep_a = models.CharField(max_length=3)
    concep_b = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    id_clase_pagos = models.ForeignKey(ClasePagos, models.DO_NOTHING, db_column='id_clase_pagos', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'concepto'


class Configuracion(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    id_clase_pagos = models.ForeignKey(ClasePagos, models.DO_NOTHING, db_column='id_clase_pagos', blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configuracion'


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nom_curso = models.CharField(max_length=100)
    id_programa = models.ForeignKey('Programa', models.DO_NOTHING, db_column='id_programa')
    numciclo = models.CharField(max_length=2)
    numcreditaje = models.CharField(max_length=2)
    tipocurso = models.CharField(max_length=1)
    planestudios = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'curso'


class DatosAcademicos(models.Model):
    id_dat_academicos = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey('Docente', models.DO_NOTHING, db_column='id_docente')
    id_tip_grado = models.ForeignKey('TipoGrado', models.DO_NOTHING, db_column='id_tip_grado')
    mencion_grado = models.CharField(max_length=60)
    centro_estudios = models.CharField(max_length=60)
    pais_estudios = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'datos_academicos'


class Dia(models.Model):
    id_dia = models.CharField(primary_key=True, max_length=1)
    nom_dia = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'dia'


class Directiva(models.Model):
    id_direc = models.SmallIntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    codigo = models.CharField(unique=True, max_length=8)
    dni = models.CharField(unique=True, max_length=8)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'directiva'


class Disponibilidad(models.Model):
    id_disponibilidad = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey('Docente', models.DO_NOTHING, db_column='id_docente')
    id_dia = models.ForeignKey(Dia, models.DO_NOTHING, db_column='id_dia')
    hr_inicio = models.CharField(max_length=2)
    hr_fin = models.CharField(max_length=2)
    tot_hrs = models.CharField(max_length=2)
    id_ciclo = models.ForeignKey(Ciclo, models.DO_NOTHING, db_column='id_ciclo')

    class Meta:
        managed = False
        db_table = 'disponibilidad'


class Docente(models.Model):
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
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


class Facultad(models.Model):
    id_facultad = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'facultad'


class MAlumno(models.Model):
    dni_m = models.CharField(primary_key=True, max_length=8)
    ape_materno_m = models.CharField(max_length=60, blank=True, null=True)
    ape_paterno_m = models.CharField(max_length=60, blank=True, null=True)
    nombre_m = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm_alumno'


class Modulo(models.Model):
    id_mod = models.SmallIntegerField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'modulo'


class Perfil(models.Model):
    id_perfil = models.SmallIntegerField(primary_key=True)
    nombre_tipo = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'perfil'


class PerfilModulo(models.Model):
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil', primary_key=True)
    id_mod = models.ForeignKey(Modulo, models.DO_NOTHING, db_column='id_mod')
    estado_pm = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'perfil_modulo'
        unique_together = (('id_perfil', 'id_mod'),)


class Preferencia(models.Model):
    id_preferencia = models.AutoField(primary_key=True)
    id_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='id_docente')
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_curso')
    id_ciclo = models.ForeignKey(Ciclo, models.DO_NOTHING, db_column='id_ciclo')

    class Meta:
        managed = False
        db_table = 'preferencia'


class Programa(models.Model):
    id_programa = models.SmallIntegerField(primary_key=True)
    nom_programa = models.CharField(max_length=116)
    sigla_programa = models.CharField(max_length=10)
    id_tip_grado = models.ForeignKey('TipoGrado', models.DO_NOTHING, db_column='id_tip_grado')
    vigencia_programa = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'programa'


class Recaudaciones(models.Model):
    id_rec = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_alum = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alum')
    id_concepto = models.ForeignKey(Concepto, models.DO_NOTHING, db_column='id_concepto')
    id_registro = models.ForeignKey('RegistroCarga', models.DO_NOTHING, db_column='id_registro')
    id_programa = models.SmallIntegerField(blank=True, null=True)
    id_ubicacion = models.ForeignKey('Ubicacion', models.DO_NOTHING, db_column='id_ubicacion', blank=True, null=True)
    cod_alumno = models.ForeignKey(AlumnoPrograma, models.DO_NOTHING, db_column='cod_alumno', blank=True, null=True)
    moneda = models.CharField(max_length=3, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carnet = models.CharField(max_length=30, blank=True, null=True)
    autoseguro = models.CharField(max_length=30, blank=True, null=True)
    ave = models.CharField(max_length=30, blank=True, null=True)
    devol_tran = models.CharField(max_length=30, blank=True, null=True)
    observacion = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    validado = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'recaudaciones'


class RecaudacionesFallidas(models.Model):
    id_fallidas = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    id_registro = models.ForeignKey('RegistroCarga', models.DO_NOTHING, db_column='id_registro', blank=True, null=True)
    nombre_archivo = models.CharField(max_length=100, blank=True, null=True)
    descripcion_error = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recaudaciones_fallidas'


class RecaudacionesRaw(models.Model):
    id_raw = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    moneda = models.CharField(max_length=3, blank=True, null=True)
    dependencia = models.CharField(max_length=50, blank=True, null=True)
    concep = models.CharField(max_length=6, blank=True, null=True)
    concep_a = models.CharField(max_length=3, blank=True, null=True)
    concep_b = models.CharField(max_length=3, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    codigo = models.CharField(max_length=15, blank=True, null=True)
    nombre = models.CharField(max_length=300, blank=True, null=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carnet = models.CharField(max_length=30, blank=True, null=True)
    autoseguro = models.CharField(max_length=30, blank=True, null=True)
    ave = models.CharField(max_length=30, blank=True, null=True)
    devol_tran = models.CharField(max_length=30, blank=True, null=True)
    observacion = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recaudaciones_raw'


class RegistroCarga(models.Model):
    id_registro = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    nombre_equipo = models.CharField(max_length=70, blank=True, null=True)
    ip = models.CharField(max_length=30, blank=True, null=True)
    ruta = models.CharField(max_length=200, blank=True, null=True)
    fecha_carga = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registro_carga'


class TipoGrado(models.Model):
    id_tip_grado = models.CharField(primary_key=True, max_length=2)
    nom_tip_grado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_grado'


class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ubicacion'


class Usuario(models.Model):
    id_usuario = models.DecimalField(primary_key=True, max_digits=65535, decimal_places=65535)
    user_name = models.CharField(unique=True, max_length=300)
    pass_field = models.CharField(db_column='pass', max_length=50)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'usuario'


class UsuarioModulo(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_mod = models.ForeignKey(Modulo, models.DO_NOTHING, db_column='id_mod')
    estado_um = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'usuario_modulo'
        unique_together = (('id_usuario', 'id_mod'),)


class UsuarioPerfil(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')
    estado_up = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'usuario_perfil'
        unique_together = (('id_usuario', 'id_perfil'),)
