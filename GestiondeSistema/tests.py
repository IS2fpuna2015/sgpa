# Create your tests here.
from unittest import TestCase

from .models import Sistema


class SistemaTestCase(TestCase):
    def setUp(self):
            re = Sistema()
            re.registrar("Asignacion de US ","anonimo","Ninguno")
            re.registrar("Creacion de US ","anonimo","Ninguno")
            re.registrar("Modificacion de US ","anonimo","Ninguno")

    def test_listar_registro(self):
        Sistema.objects.all()
        print("Listar registro sin problemas")