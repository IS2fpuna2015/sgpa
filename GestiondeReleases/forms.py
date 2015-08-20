from django import forms

class Release_Buscar_form(forms.Form):
    Busqueda = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False)