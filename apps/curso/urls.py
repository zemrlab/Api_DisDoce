from django.urls import path
from apps.curso import views


app_name='curso'

urlpatterns = [
    path('api', views.ProgramasCursoList.as_view(),name='api'),
    path('docente/<pk>',views.ProgramaDocenteLista.as_view(),name='docente_curso'),
]
