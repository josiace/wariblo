from django.contrib import admin
from django.utils.html import format_html
from .models import Country, Currency


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['get_flag', 'name', 'code', 'phone_code', 'get_currency', 'is_active', 'created_at']
    list_filter = ['is_active', 'currency']
    search_fields = ['name', 'code', 'phone_code']
    list_editable = ['is_active']
    list_per_page = 20
    ordering = ['name']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'code', 'flag_emoji', 'phone_code')
        }),
        ('Devise', {
            'fields': ('currency',)
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    def get_flag(self, obj):
        return format_html('<span style="font-size: 24px;">{}</span>', obj.flag_emoji)
    get_flag.short_description = 'Drapeau'
    
    def get_currency(self, obj):
        if obj.currency:
            return format_html('<span style="color: #FF4500; font-weight: bold;">{} {}</span>', 
                             obj.currency.symbol, obj.currency.code)
        return '—'
    get_currency.short_description = 'Devise'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['get_symbol', 'code', 'name', 'exchange_rate_to_usd', 'last_updated', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name']
    list_editable = ['is_active', 'exchange_rate_to_usd']
    readonly_fields = ['last_updated']
    list_per_page = 20
    ordering = ['code']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'name', 'symbol')
        }),
        ('Taux de change', {
            'fields': ('exchange_rate_to_usd',)
        }),
        ('Statut', {
            'fields': ('is_active', 'last_updated')
        }),
    )
    
    def get_symbol(self, obj):
        return format_html('<span style="font-size: 20px; color: #FF4500; font-weight: bold;">{}</span>', obj.symbol)
    get_symbol.short_description = 'Symbole'

