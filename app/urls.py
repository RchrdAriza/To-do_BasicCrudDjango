from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('tareas/', views.listar_tareas, name='tareas'),
    path('signup/', views.signup, name='signup'),
    path('tareas/crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('logout/', views.signout, name='signout'),
    path('tareas/modificar_tarea/<id>', views.modificar_tarea, name='modificar_tarea'),
    path('eliminar/<id>', views.eliminar_tarea, name='eliminar_tarea'),
    path('ver_tarea/<id>', views.ver_tarea, name='ver_tarea'),
]
