from django import forms
from django.forms import ModelForm, DateInput
from .models import Sprint


class sprint_form(ModelForm):

    class Meta:
        model = Sprint
        fields = ['nombre_sprint', 'fecha_inicio', 'fecha_fin',]
        exclude= ('numero_sprint', )
        widgets = {
                    'fecha_inicio': DateInput(attrs={'class': 'datepicker'}),
                    'fecha_fin': DateInput(attrs={'class': 'datepicker'}),}

class modificar_sprint_form(ModelForm):

    class Meta:
        model = Sprint
        fields = ['nombre_sprint', 'fecha_inicio', 'fecha_fin','estado']
        exclude= ('numero_sprint', )
        widgets = {
                    'fecha_inicio': DateInput(attrs={'class': 'datepicker'}),
                    'fecha_fin': DateInput(attrs={'class': 'datepicker'}),}




class Busqueda_sprint_form(forms.Form):
    Busqueda = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}), required=False)