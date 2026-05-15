from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'requirements', 'budget', 'niche', 'platform', 'deadline', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'budget': forms.NumberInput(attrs={'step': '0.01'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget <= 0:
            raise ValidationError("Le budget doit être supérieur à 0.")
        return budget
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < date.today():
            raise ValidationError("La date limite ne peut pas être dans le passé.")
        return deadline
