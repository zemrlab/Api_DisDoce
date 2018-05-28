from django.urls import path
from apps.curso import views


app_name='curso'

urlpatterns = [
    path('cursos', views.ProgramasCursoList.as_view(),name='api'),
    path('docente/<pk>',views.ProgramaDocenteLista.as_view(),name='docente_curso'),
    path('ciclos', views.CicloList.as_view(), name='Ciclo_list'),
    path('cicloshabilitados', views.CicloListHabilitados.as_view(), name='Ciclo_list_habilitados'),
    path('nuevociclo', views.CicloCreate.as_view(), name='Ciclo_create'),
    path('ciclo/<pk>', views.CicloGetUpdate.as_view(), name='Ciclo_get_update'),
]
