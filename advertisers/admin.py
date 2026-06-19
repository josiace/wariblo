from django.contrib import admin
from django.utils.html import format_html
from .models import AdvertiserProfile


@admin.register(AdvertiserProfile)
class AdvertiserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_company', 'get_email', 'get_industry', 'location', 'get_logo', 'created_at']
    list_filter = ['industry', 'location', 'created_at']
    search_fields = ['company_name', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user', 'company_name')
        }),
        ('Profil annonceur', {
            'fields': ('industry', 'description', 'location')
        }),
        ('Site web', {
            'fields': ('website',)
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_company(self, obj):
        return format_html('<strong>{}</strong>', obj.company_name)
    get_company.short_description = 'Entreprise'
    
    def get_email(self, obj):
        return obj.user.email if obj.user else '—'
    get_email.short_description = 'Email'
    
    def get_industry(self, obj):
        industry_colors = {
            'fashion': '#FF1493',
            'tech': '#00CED1',
            'food': '#FF6347',
            'health': '#32CD32',
            'finance': '#4682B4',
            'education': '#4169E1',
            'entertainment': '#FF4500',
            'travel': '#1E90FF',
            'beauty': '#FF69B4',
            'fitness': '#32CD32',
            'automotive': '#FF6347',
            'retail': '#FFD700',
            'other': '#666',
        }
        color = industry_colors.get(obj.industry, '#666')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_industry_display())
    get_industry.short_description = 'Industrie'
    
    def get_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 8px; object-fit: cover;" />', obj.logo.url)
        return '—'
    get_logo.short_description = 'Logo'

