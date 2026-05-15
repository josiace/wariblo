from django import forms
from django.core.exceptions import ValidationError
from .models import AdvertiserProfile


class AdvertiserProfileForm(forms.ModelForm):
    class Meta:
        model = AdvertiserProfile
        fields = ['company_name', 'industry', 'website', 'description', 'logo', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            raise ValidationError("Website URL must start with http:// or https://")
        return website
