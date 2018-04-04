from django.db import models

# Create your models here.

class TipoUsuario(models.Model):
    id_tu = models.IntegerField(primary_key=True)
    nombre_tipo = models.CharField(unique=True, max_length=30)

    class Meta:
        #managed = False
        db_table = 'tipo_usuario'
class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    id_tu = models.ForeignKey(TipoUsuario, db_column='id_tu',on_delete=models.CASCADE)
    user_name = models.CharField(unique=True, max_length=30)
    pass_field = models.CharField(db_column='pass', max_length=30)  # Field renamed because it was a Python reserved word.

    class Meta:
        #managed = False
        db_table = 'usuario'