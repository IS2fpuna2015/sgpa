#encoding:utf-8
from django.test import TestCase

from GestiondeUsuarios.models import Usuario


class UsuarioTestCase(TestCase):
    def setUp(self):
        print ("\nPrueba de creacion de usuarios")
        Usuario.objects.create(username="test",first_name="admin", last_name="planas", telefono="637251")
        Usuario.objects.create(username="usuario1",first_name="nombre1", last_name="apellido1")
        Usuario.objects.create(username="usuario2",first_name="nombre2", last_name="apellido2")
        Usuario.objects.create(username="usuario3",first_name="nombre3", last_name="apellido3")
        print ("Sin errores de creacion")


    def test_consulta_usuario(self):
        print ("\nPrueba de busqueda y consulta de usuarios creados")
        self.user = Usuario.objects.get(username='usuario3')
        self.user = Usuario.objects.get(last_name='apellido1')
        self.user = Usuario.objects.get(first_name='nombre2')
        self.user = Usuario.objects.get(telefono='637251')
        print ("Sin errores de consulta")


    def test_listar_usuario(self):
        print ("\nPrueba para obtener todos los usuarios")
        Usuario.objects.all()
        print ("Sin errores de listado")

    def test_eliminacion_usuario(self):
        print ("\nPrueba de elimanacion de usuarios creados")
        Usuario.objects.get(username='usuario3').delete()
        Usuario.objects.get(first_name="nombre1").delete()
        Usuario.objects.get(first_name='nombre2').delete()
        Usuario.objects.get(telefono='637251').delete()
        print ("Sin errores de eliminacion")
