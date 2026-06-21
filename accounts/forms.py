from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User
from core.models import Country


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = forms.CharField(required=True, max_length=20)
    country = forms.ModelChoiceField(queryset=Country.objects.filter(is_active=True), required=True)
    username = forms.CharField(required=False, widget=forms.HiddenInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone_number', 'country', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà enregistré.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.phone_number = self.cleaned_data['phone_number']
        user.country = self.cleaned_data['country']
        # Générer un username automatiquement à partir de l'email
        if not user.username:
            user.username = self.cleaned_data['email'].split('@')[0]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
