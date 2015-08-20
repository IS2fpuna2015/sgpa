import base64
from GestiondeUserStories import models
from django.core import files
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse
import os
from io import StringIO

class DatabaseStorage(Storage):
    def _generar_nombre(self, name, pk):
        """
        Cambia el nombre del archivo con el especificado en el parametro pk
        y elimina cualquier directorio
        :param name:
        :param pk:
        :return:
        """
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        return '%s%s' % (pk,file_ext)

    def _open(self, name, mode='rb'):
        try:
            archivo = models.File.objects.get_from_name(name)
        except models.File.DoesNotExist:
            return None
        archivo_hash = StringIO.StringIO(base64.b64decode(archivo.content))
        archivo_hash.name = name
        archivo_hash.mode = mode
        archivo_hash.size = archivo.size
        return files.File(archivo_hash)

    def _save(self, name, content):
        archivo = models.File.objects.create(
            content = base64.b64encode(content.read()),
            size = content.size,
        )
        return self._generar_nombre(name, archivo.pk)

    def exists(self, name):
        """
        Generamos un nuevo nombre para cada archivo, por lo que nunca estara
        en existencia previamente.
        :param name:
        :return:
        """
        return False

    def delete(self, name):
        try:
            models.File.objects.get_from_name(name).delete()
        except models.File.DoesNotExist:
            pass

    def url(self, name):
        return reverse('archivo_db', kwargs={'name':name})

    def size(self, name):
        try:
            return models.File.objects.get_from_name(name).size
        except models.File.DoesNotExist:
            return 0
