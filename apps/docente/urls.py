from django.urls import path
from apps.docente import views


app_name='docente'

urlpatterns = [
    path('api/<id>', views.DocenteGet.as_view(), name='api'),
    path('pdf/<id>', views.PDFView.as_view(), name='pdf_docente'),
]
