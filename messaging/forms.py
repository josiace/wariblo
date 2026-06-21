from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Message
import re


def has_long_digit_sequence(text, max_length=4):
    """Détecte si le texte contient une séquence de chiffres plus longue que max_length"""
    # Trouver toutes les séquences de chiffres
    digit_sequences = re.findall(r'\d+', text)
    for sequence in digit_sequences:
        if len(sequence) > max_length:
            return True
    return False


def has_phone_patterns(text):
    """Détecte les patterns de numéros de téléphone"""
    phone_patterns = [
        r'\+\d{1,3}[\s-]?\d{8,}',  # Format international: +33 6 12 34 56 78
        r'\d{2}[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}',  # Format français: 06 12 34 56 78
        r'\d{3}[\s-]?\d{3}[\s-]?\d{4}',  # Format US: 123-456-7890
        r'\d{10,}',  # Séquence de 10+ chiffres
        r'0[1-9][\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}',  # Format mobile français
    ]
    
    for pattern in phone_patterns:
        if re.search(pattern, text):
            return True
    return False


def has_contact_keywords(text):
    """Détecte les mots-clés liés aux coordonnées"""
    keywords = [
        'téléphone', 'tel', 'mobile', 'portable', 'whatsapp', 'wa', 
        'appel', 'appelle', 'téléphoner', 'numéro', 'numero', 'num',
        'sms', 'texte', 'viber', 'telegram', 'signal', 'discord',
        'instagram', 'facebook', 'snapchat', 'tiktok', 'twitter',
        'email', 'mail', '@', 'gmail', 'yahoo', 'hotmail', 'outlook',
        'skype', 'zoom', 'meet', 'facetime', 'call'
    ]
    
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False


def has_external_links(text):
    """Détecte les liens externes"""
    url_pattern = r'https?://[^\s]+|www\.[^\s]+'
    return bool(re.search(url_pattern, text))


def censor_contact_info(text):
    """Censure les informations de contact dans le texte"""
    # Censure les séquences de chiffres
    text = re.sub(r'\d{5,}', '*****', text)
    # Censure les patterns de téléphone
    text = re.sub(r'\+\d{1,3}[\s-]?\d{8,}', '*****', text)
    # Censure les emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '*****', text)
    # Censure les URLs
    text = re.sub(r'https?://[^\s]+|www\.[^\s]+', '*****', text)
    return text


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
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise ValidationError("Le message ne peut pas être vide.")
        if len(content) > 5000:
            raise ValidationError("Le message ne peut pas dépasser 5000 caractères.")
        
        # Vérifier les limitations selon le plan d'abonnement
        if self.user:
            from core.models import Subscription
            
            # Vérifier si l'utilisateur a un abonnement actif
            active_subscription = Subscription.objects.filter(
                user=self.user,
                status='active',
                end_date__gt=timezone.now()
            ).first()
            
            # Si pas d'abonnement actif ou plan gratuit, appliquer les limitations
            if not active_subscription or active_subscription.plan.plan_type == 'free':
                # Vérifier les séquences de chiffres (max 4 chiffres successifs)
                if has_long_digit_sequence(content, max_length=4):
                    raise ValidationError(
                        "Pour des raisons de sécurité, les utilisateurs du plan gratuit ne peuvent pas envoyer "
                        "de numéros de téléphone ou d'autres coordonnées personnelles dans les messages. "
                        "Passez à un plan payant pour bénéficier de cette fonctionnalité."
                    )
                
                # Vérifier les patterns de téléphone
                if has_phone_patterns(content):
                    raise ValidationError(
                        "Pour des raisons de sécurité, les utilisateurs du plan gratuit ne peuvent pas envoyer "
                        "de numéros de téléphone dans les messages. Passez à un plan payant pour bénéficier de cette fonctionnalité."
                    )
                
                # Vérifier les mots-clés de contact
                if has_contact_keywords(content):
                    raise ValidationError(
                        "Pour des raisons de sécurité, les utilisateurs du plan gratuit ne peuvent pas mentionner "
                        "des applications de messagerie ou de contact dans les messages. Passez à un plan payant pour bénéficier de cette fonctionnalité."
                    )
                
                # Vérifier les liens externes
                if has_external_links(content):
                    raise ValidationError(
                        "Pour des raisons de sécurité, les utilisateurs du plan gratuit ne peuvent pas envoyer "
                        "de liens externes dans les messages. Passez à un plan payant pour bénéficier de cette fonctionnalité."
                    )
            else:
                # Pour les utilisateurs payants, appliquer la censure automatique
                censored_content = censor_contact_info(content)
                if censored_content != content:
                    # Avertir l'utilisateur que le message a été censuré
                    self.cleaned_data['content'] = censored_content
        
        return content.strip()
