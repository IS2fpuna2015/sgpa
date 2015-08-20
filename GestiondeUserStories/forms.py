from django.forms import ModelForm, ChoiceField, Select, ModelChoiceField, RadioSelect, TextInput, Textarea, CharField, \
    Form, IntegerField, Form, IntegerField, FileField
from GestiondeUserStories.models import UserStory
from GestiondeSprints.models import Sprint

ESTADOS = (
    ('PENDIENTE', 'Pendiente'),
    ('ANULADO', 'Anulado'),
    ('ENCURSO', 'En Curso'),
    ('RESUELTO', 'Resuelto'),
    ('APROBADO', 'Aprobado')
)

PORCENTAJES = (
    (0, '0 %'),
    (10, '10 %'),
    (20, '20 %'),
    (30, '30 %'),
    (40, '40 %'),
    (50, '50 %'),
    (60, '60 %'),
    (70, '70 %'),
    (80, '80 %'),
    (90, '90 %'),
    (100, '100 %'),

)

VALORES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),

)


PRIORIDAD = (
    ('ALTA', 'Alta'),
    ('NORMAL', 'Normal'),
    ('BAJA', 'Baja'),
)



class CrearUserStoryForm(ModelForm):
    def __init__(self, proyecto, *args, **kwargs):
        super(CrearUserStoryForm, self).__init__(*args, **kwargs)
        #self.fields['usuario_asignado'] = ModelChoiceField(queryset=proyecto.equipo_desarrollo.all(),
         #                                                  widget=RadioSelect, empty_label="Ninguno",
          #                                                 required=False)

    nombre = CharField(widget=TextInput(attrs={'class': 'special'}), required=True)
    descripcion = CharField(widget=Textarea(attrs={'rows': 3, 'cols': 30}), required=True)
    prioridad = ChoiceField(choices=PRIORIDAD, widget=Select, initial='Baja')
    valor_tecnico = ChoiceField(choices=VALORES, widget=Select, initial='1')
    valor_de_negocio = ChoiceField(choices=VALORES, widget=Select, initial='1')
    size = IntegerField(min_value=1, max_value=30)

    class Meta:
        model = UserStory
        fields = (
            'nombre', 'descripcion', 'prioridad', 'valor_tecnico', 'valor_de_negocio', 'size', 'usuario_asignado',)


class ModificarUserStoryForm(ModelForm):

    def __init__(self, proyecto,estado,porcentaje,sprint_inicial, *args, **kwargs):
        super(ModificarUserStoryForm, self).__init__(*args, **kwargs)
        self.fields['usuario_asignado'] = ModelChoiceField(queryset=proyecto.equipo_desarrollo.all(),
                                                           widget=RadioSelect, empty_label="Ninguno",
                                                           required=False)
        self.fields['estado'] = ChoiceField(choices=ESTADOS, widget=Select, initial=estado)
        self.fields['porcentaje_realizado'] = ChoiceField(choices=PORCENTAJES, widget=Select, initial=porcentaje)
        self.fields['sprint'] = ModelChoiceField(queryset=Sprint.objects.filter(id_proyecto_id=proyecto.id),
                                                 widget=Select,initial=sprint_inicial)

    nombre = CharField(widget=TextInput(attrs={'class': 'special'}), required=True)
    descripcion = CharField(widget=Textarea(attrs={'rows': 3, 'cols': 30}), required=True)
    prioridad = ChoiceField(choices=PRIORIDAD, widget=Select, initial='Baja')
    valor_tecnico = ChoiceField(choices=VALORES, widget=Select, initial='1')
    valor_de_negocio = ChoiceField(choices=VALORES, widget=Select, initial='1')
    size = IntegerField(min_value=1, max_value=60)
    horas_trabajadas  =  IntegerField(min_value=0,initial=0)

    class Meta:
        model = UserStory
        fields = (
            'nombre', 'descripcion', 'prioridad', 'valor_tecnico', 'valor_de_negocio', 'size', 'usuario_asignado','estado','porcentaje_realizado')



class ModificarUserStoryFormDesarrollador(Form):

    def __init__(self,estado,porcentaje, *args, **kwargs):
        super(ModificarUserStoryFormDesarrollador, self).__init__(*args, **kwargs)
        self.fields['estado'] = ChoiceField(choices=ESTADOS, widget=Select, initial=estado)
        self.fields['porcentaje_realizado'] = ChoiceField(choices=PORCENTAJES, widget=Select, initial=porcentaje)

    horas_trabajadas  =  IntegerField(min_value=0)


class Busqueda_UserStory_form(Form):
    Busqueda = CharField(widget=TextInput(attrs={'class':'special'}), required=False)

class FileAttached_form(Form):
    image = FileField(label='Elige un archivo')
