from django.urls import path
from apps.disponibilidad import views


app_name='disponibilidad'

urlpatterns = [
    path('api/<pk>/<ciclo>', views.DisponibilidadList.as_view(), name='api_devolver'),
    path('dias',views.DiaList.as_view(),name='dia_list'),
]
