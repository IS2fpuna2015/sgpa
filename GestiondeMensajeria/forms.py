from django.db.models import Q
from django.forms import Form, Select, CharField, TextInput, Textarea, ModelChoiceField
from GestiondeUsuarios.models import Usuario


class CrearMensajeForm(Form):

    def __init__(self,username, *args, **kwargs):
        super(CrearMensajeForm, self).__init__(*args, **kwargs)
        self.fields['destinatario'] = ModelChoiceField(queryset=Usuario.objects.filter(~Q(username=username)),widget=Select(), empty_label=None)

    asunto = CharField(widget=TextInput(), required=True)
    mensaje = CharField(widget=Textarea(attrs={'rows': 3, 'cols': 30}), required=True)

class BuscarMensajeForm(Form):
    busqueda = CharField(widget=TextInput(attrs={'class':'special'}), required=False)