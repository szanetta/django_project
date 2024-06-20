from django import forms
from . import models

class SurrenderPet(forms.ModelForm):
    class Meta:
        model = models.Pet
        fields = [
            'name',
            'size',
            'breed',
            'gender',
            'age',
            'characteristics',
            'overall_health',
            'good_in_home_with',
            'banner'
        ]
