from django import forms



class Busqueda_Auditoria_form(forms.Form):
    Busqueda = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False ,)


