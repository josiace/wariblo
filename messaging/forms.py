from django import forms
from django.core.exceptions import ValidationError
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tapez votre message...',
                'class': 'form-control'
            }),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise ValidationError("Le message ne peut pas être vide.")
        if len(content) > 5000:
            raise ValidationError("Le message ne peut pas dépasser 5000 caractères.")
        return content.strip()
