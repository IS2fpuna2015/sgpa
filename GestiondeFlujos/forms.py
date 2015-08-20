from django import forms
class crear_flujo_form(forms.Form):
    nombre_flujo = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False, label='Nombre del Flujo')

class crear_actividad_form(forms.Form):
    OPTIONS = (
        ('todo','To Do'),
        ('doing','Doing'),
        ('done','Done'),
        ('0','-----')

    )
    nombre_actividad = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False, label='Nombre de la Actividad')
    estado_actividad = forms.ChoiceField(widget=forms.Select(attrs={'disabled':'disabled'}), choices=OPTIONS, required=True, initial='todo', )
    orden_actividad = forms.IntegerField(required=False)

class Busqueda_flujo_form(forms.Form):
    Busqueda = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False)

class modificar_actividad_form(forms.Form):
    OPTIONS = (
        ('todo','To Do'),
        ('doing','Doing'),
        ('done','Done'),
        ('0','-----')

    )
    nombre_actividad = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False, label='Nombre de la Actividad')
    estado_actividad = forms.ChoiceField(widget=forms.Select, choices=OPTIONS, required=True, initial='todo', )
    orden_actividad = forms.IntegerField(required=False)