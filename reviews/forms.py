from django import forms
from django.core.exceptions import ValidationError
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Partagez votre expérience...',
                'class': 'form-control'
            }),
        }
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise ValidationError("Votre commentaire doit contenir au moins 10 caractères.")
        if len(comment) > 500:
            raise ValidationError("Votre commentaire ne peut pas dépasser 500 caractères.")
        return comment
