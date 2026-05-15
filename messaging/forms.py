from django import forms
from django.core.exceptions import ValidationError
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise ValidationError("Message cannot be empty.")
        if len(content) > 5000:
            raise ValidationError("Message cannot exceed 5000 characters.")
        return content.strip()
