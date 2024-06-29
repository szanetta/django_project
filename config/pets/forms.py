from django import forms
from . import models
from .models import Application

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
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant_email', 'message', 'pet']
        labels = {'applicant_email': 'Your Email',
            'message': 'Message'
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.pet = kwargs.pop('pet', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        pet = self.cleaned_data.get('pet')
        applicant_email = self.cleaned_data.get('applicant_email')
        # sprawdzenie, czy istnieje już wniosek dla tego samego zwierzaka i tego samego maila
        existing_application = None

        try:
            existing_application = Application.objects.get(pet=pet, applicant_email=applicant_email)
        except Application.DoesNotExist:
            pass

        if existing_application:
            raise forms.ValidationError('You have already submitted an application for this pet.')