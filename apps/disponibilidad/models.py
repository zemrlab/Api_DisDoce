from django.db import models
from apps.docente.models import Docente
from apps.curso.models import Ciclo
# Create your models here.

class Dia(models.Model):
    id_dia = models.CharField(primary_key=True, max_length=1)
    nom_dia = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'dia'
class Disponibilidad(models.Model):
    id_disponibilidad = models.IntegerField(primary_key=True)
    id_docente = models.ForeignKey(Docente, db_column='id_docente',on_delete=models.CASCADE)
    id_dia = models.ForeignKey(Dia, db_column='id_dia',on_delete=models.CASCADE)
    hr_inicio = models.CharField(max_length=2)
    hr_fin = models.CharField(max_length=2)
    tot_hrs = models.CharField(max_length=2)
    id_ciclo = models.ForeignKey(Ciclo,default=1, db_column='id_ciclo',on_delete=models.CASCADE)
    #id_ciclo=models.IntegerField(primary_key=True);
    class Meta:
        managed = False
        db_table = 'disponibilidad'


