from django import forms
from django.forms import ModelForm, DateInput, Textarea, ModelChoiceField, RadioSelect, CheckboxSelectMultiple, \
    ModelMultipleChoiceField, CharField, TextInput, ChoiceField, Select

from GestiondeProyectos.models import Proyecto
from GestiondeUsuarios.models import Usuario
from django.contrib.auth.models import Group


class CrearProyectoForm(ModelForm,forms.Form):

    estado_proyecto = CharField(widget=TextInput(attrs={'readonly': True,'value':'PENDIENTE'}),)
    scrum_master = ModelChoiceField(initial=2, queryset=Usuario.objects.filter(groups=Group.objects.get(name='Scrum Master').id).filter(is_active="True"),widget=RadioSelect)
    equipo_desarrollo = ModelMultipleChoiceField(queryset=Usuario.objects.filter(groups=Group.objects.get(name='Desarrollador').id).filter(is_active="True"), widget=CheckboxSelectMultiple)
    cliente = ModelChoiceField(initial=2,queryset=Usuario.objects.filter(groups=Group.objects.get(name='Cliente').id).filter(is_active="True"), widget=RadioSelect)

    class Meta:
        model = Proyecto

        fields = ('nombre_proyecto', 'codigo_proyecto', 'descripcion_proyecto',
                    'fecha_inicio', 'fecha_finalizacion', 'scrum_master', 'equipo_desarrollo','estado_proyecto','cliente')
        exclude= ('id_proyecto','cantidad_sprints')
        widgets = {
                    'fecha_inicio': DateInput(attrs={'class': 'datepicker'}),
                   'fecha_finalizacion': DateInput(attrs={'class': 'datepicker'}),
                   'descripcion_proyecto': Textarea(attrs={'rows': 3, 'cols': 30})}

class Proyecto_Buscar_form(forms.Form):
    Busqueda = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False)


class ModificarProyectoForm(CrearProyectoForm):

    #Utiliza la clase Meta para agregar el atributo de readonly
    class Meta:
        model = Proyecto
        fields = ('nombre_proyecto', 'codigo_proyecto', 'descripcion_proyecto',
                    'fecha_inicio', 'fecha_finalizacion','scrum_master', 'equipo_desarrollo','estado_proyecto','cliente',)
        exclude= ('id_proyecto',)
        widgets = {
                    'nombre_proyecto': TextInput(attrs={'readonly': 'True'}),
                    'cliente':  Select(attrs={'readonly': 'readonly'}),
                    'codigo_proyecto': TextInput(attrs={'readonly': 'True'}),
                    'fecha_inicio': DateInput(attrs={'class': 'datepicker', 'readonly': 'True'}),
                    'fecha_finalizacion': DateInput(attrs={'class': 'datepicker'}),
                    'descripcion_proyecto': Textarea(attrs={'rows': 3, 'cols': 30})}


    ESTADOS = (
        ('PENDIENTE','Pendiente'),
        ('ACTIVO','Activo'),
        ('CANCELADO','Cancelado'),
        ('FINALIZADO','Finalizado')
    )

    estado_proyecto = ChoiceField(choices=ESTADOS, widget=Select)

