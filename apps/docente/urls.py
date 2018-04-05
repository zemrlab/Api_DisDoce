from django.urls import path
from apps.docente import views


app_name='docente'

urlpatterns = [
    path('api/<id>', views.DocenteList.as_view(),name='api'),
]
