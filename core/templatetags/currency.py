from django import template
from django.conf import settings
from ..models import Currency

register = template.Library()


@register.filter
def convert_currency(amount, user=None):
    """
    Convertit un montant USD vers la devise de l'utilisateur
    Si user est None, utilise la devise par défaut (USD)
    """
    if not amount:
        return amount
    
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return amount
    
    # Si pas d'utilisateur ou pas de pays, retourne en USD
    if not user or not hasattr(user, 'country') or not user.country:
        return f"${amount:,.2f}"
    
    # Récupérer la devise du pays de l'utilisateur
    currency = user.country.currency
    if not currency or not currency.is_active:
        return f"${amount:,.2f}"
    
    # Convertir le montant
    converted_amount = currency.convert_from_usd(amount)
    
    return f"{currency.symbol}{converted_amount:,.2f}"


@register.filter
def currency_symbol(user=None):
    """Retourne le symbole de la devise de l'utilisateur"""
    if not user or not hasattr(user, 'country') or not user.country:
        return "$"
    
    currency = user.country.currency
    if not currency or not currency.is_active:
        return "$"
    
    return currency.symbol


@register.simple_tag
def get_user_currency(user=None):
    """Retourne l'objet Currency de l'utilisateur"""
    if not user or not hasattr(user, 'country') or not user.country:
        return None
    
    return user.country.currency
