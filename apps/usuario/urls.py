from django.urls import path
from apps.usuario import views


app_name='usuario'

urlpatterns = [
    path('api', views.ExcelView.as_view(), name='api'),
]
