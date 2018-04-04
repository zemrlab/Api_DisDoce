from django.urls import path
from apps.disponibilidad import views


app_name='disponibilidad'

urlpatterns = [
    path('api', views.DisponibilidadList.as_view(),name='api'),
]
