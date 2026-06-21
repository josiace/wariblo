from .models import SiteSettings


def site_settings(request):
    """Context processor pour rendre les paramètres du site disponibles dans tous les templates"""
    settings_obj = SiteSettings.get_settings()
    
    return {
        'site_settings': settings_obj,
        'default_currency': settings_obj.default_currency,
        'default_currency_symbol': settings_obj.default_currency.symbol if settings_obj.default_currency else '$',
    }
