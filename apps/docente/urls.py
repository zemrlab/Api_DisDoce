from django.urls import path
from apps.docente import views


app_name='docente'

urlpatterns = [
    path('docente/<id>', views.DocenteGet.as_view(), name='api'),
    path('docentes', views.DocenteList.as_view(), name='docente_list'),
    path('pdf/<id>/<idciclo>', views.PDFView.as_view(), name='pdf_docente'),
]
