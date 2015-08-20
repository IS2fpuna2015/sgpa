from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
#"""
#Este formulario es utilizado para los filtrados y busqueda personalizada de los usuarios
#existentes en la base de datos.

#Los Roles por defecto son: Administrador, Desarrollador y Scrum Master.
#"""


class Tipos_Usuario_form(forms.Form):
    #OPTIONS = (
        #('administrador','Administrador'),
        #('desarrollador','Desarrollador'),
        #('scrumm','Scrum Master'),
        #('todos','Todos'),
        #('ninguno','-----')

    #)
    OPTIONS = queryset=Group.objects.all()
    Busqueda = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False)
    Tipos_Usuario = forms.ModelChoiceField(queryset=OPTIONS, label='Roles', required=False)





