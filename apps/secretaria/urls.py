from django.urls import path
from apps.secretaria import views


app_name='secretaria'

urlpatterns = [
    path('buscar', views.buscadorTotal.as_view(), name='api'),
    #path('consultarDocentePDF/<id>/<ciclo>', views.ConsultaDocentePDF.as_view(), name='pdf_docente'),
]
