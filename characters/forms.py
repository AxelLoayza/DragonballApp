from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'race', 'gender', 'ki', 'max_ki', 'image', 'description', 'affiliation', 'origin_planet']
