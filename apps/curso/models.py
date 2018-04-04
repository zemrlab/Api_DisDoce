from django.db import models
# Create your models here.

class Programa(models.Model):
    id_programa = models.IntegerField(primary_key=True)
    nom_programa = models.CharField(max_length=50)

    class Meta:
        #managed = False
        db_table = 'programa'


class Curso(models.Model):
    id_curso = models.IntegerField(primary_key=True)
    nom_curso = models.CharField(max_length=40)
    id_programa = models.ForeignKey(Programa, db_column='id_programa',on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'curso'


