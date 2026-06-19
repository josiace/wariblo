from django import forms
from django.core.exceptions import ValidationError
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['pitch', 'proposed_price']
        widgets = {
            'pitch': forms.Textarea(attrs={
                'rows': 6, 
                'placeholder': 'Expliquez à l\'annonceur pourquoi vous êtes le candidat idéal pour cette campagne...',
                'class': 'form-control'
            }),
            'proposed_price': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Votre prix proposé',
                'class': 'form-control'
            }),
        }
    
    def clean_pitch(self):
        pitch = self.cleaned_data.get('pitch')
        if len(pitch) < 50:
            raise ValidationError("Votre pitch doit contenir au moins 50 caractères.")
        return pitch
    
    def clean_proposed_price(self):
        price = self.cleaned_data.get('proposed_price')
        if price is not None and price <= 0:
            raise ValidationError("Le prix proposé doit être supérieur à 0.")
        return price
