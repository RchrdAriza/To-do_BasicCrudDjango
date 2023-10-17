from django import forms
from .models import Tarea

class TareasForms(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['title', 'description', 'important']
