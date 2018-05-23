from django.urls import path
from apps.curso import views


app_name='curso'

urlpatterns = [
    path('api', views.ProgramasCursoList.as_view(),name='api'),
    path('docente/<pk>',views.ProgramaDocenteLista.as_view(),name='docente_curso'),
    path('ciclos', views.CicloListCreate.as_view(), name='Ciclo_list'),
    path('nuevociclo', views.CicloCreate.as_view(), name='Ciclo_create'),
    path('ciclo/<pk>', views.CicloGetUpdate.as_view(), name='Ciclo_get_update'),
]
