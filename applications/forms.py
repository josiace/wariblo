from django import forms
from django.core.exceptions import ValidationError
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['pitch', 'proposed_price']
        widgets = {
            'pitch': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell the advertiser why you\'re the perfect fit for this campaign...'}),
            'proposed_price': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_pitch(self):
        pitch = self.cleaned_data.get('pitch')
        if len(pitch) < 50:
            raise ValidationError("Pitch must be at least 50 characters long.")
        return pitch
    
    def clean_proposed_price(self):
        price = self.cleaned_data.get('proposed_price')
        if price is not None and price <= 0:
            raise ValidationError("Proposed price must be greater than 0.")
        return price
