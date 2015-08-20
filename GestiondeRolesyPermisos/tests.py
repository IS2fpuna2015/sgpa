from django.test import TestCase
from GestiondeRolesyPermisos.models import Rol
from GestiondeUsuarios.models import Usuario

class RolesyPermisosTestCase(TestCase):

    def test_crear_rol(self):
        print("\nTEST: Crear rol")
        nombre_rol ='prueba'
        try:
            rol = Rol(name=nombre_rol)
            rol.save()
        except:
            print("Prueba fallida, no se pudo crear el rol")
            return
        if len(Rol.objects.all()) == 1:
            print("Prueba exitosa, el rol fue creado correctamente")
        else:
            print("Prueba fallida, no se pudo crear el rol")

    def test_eliminar_rol(self):
         print("\nTEST: Eliminar rol")
         nombre_rol='prueba'
         rol = Rol(name=nombre_rol)
         rol.save()

         Rol.objects.get(name=nombre_rol).delete()

         if len(Rol.objects.all())==0:
            print("Sin errores en la eliminacion ")
         else:
            print("Error en la eliminacion ")

    def test_modificar_rol(self):
         print("\nTEST: Modificar rol")
         nombre_rol='prueba'
         rol = Rol(name=nombre_rol)
         rol.save()

         rol_recuperado= Rol.objects.get(name=nombre_rol)
         rol_recuperado.name='modificado'
         rol_recuperado.save()

         if len(Rol.objects.filter(name='modificado'))==1:
            print("Sin errores en la modificacion ")
         else:
            print("Error en la modificacion ")
