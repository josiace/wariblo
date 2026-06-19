from django.contrib import admin
from django.utils.html import format_html
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['get_title', 'get_advertiser', 'get_niche', 'get_platform', 'get_budget', 'get_status', 'deadline', 'created_at']
    list_filter = ['status', 'platform', 'niche', 'created_at']
    search_fields = ['title', 'advertiser__company_name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'applications_count']
    list_per_page = 20
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('advertiser', 'title', 'niche', 'platform')
        }),
        ('Détails de la campagne', {
            'fields': ('description', 'requirements')
        }),
        ('Budget et planning', {
            'fields': ('budget', 'deadline')
        }),
        ('Statut', {
            'fields': ('status',)
        }),
        ('Statistiques', {
            'fields': ('applications_count',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_title(self, obj):
        return format_html('<strong>{}</strong>', obj.title)
    get_title.short_description = 'Titre'
    
    def get_advertiser(self, obj):
        return obj.advertiser.company_name if obj.advertiser else '—'
    get_advertiser.short_description = 'Annonceur'
    
    def get_niche(self, obj):
        niche_colors = {
            'fashion': '#FF1493',
            'tech': '#00CED1',
            'lifestyle': '#FFD700',
            'fitness': '#32CD32',
            'food': '#FF6347',
            'travel': '#1E90FF',
            'beauty': '#FF69B4',
            'gaming': '#9400D3',
            'education': '#4169E1',
            'entertainment': '#FF4500',
            'business': '#4682B4',
            'other': '#666',
        }
        color = niche_colors.get(obj.niche, '#666')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.niche)
    get_niche.short_description = 'Niche'
    
    def get_platform(self, obj):
        platform_icons = {
            'instagram': '📷',
            'tiktok': '🎵',
            'youtube': '📺',
            'twitter': '🐦',
            'facebook': '👤',
            'multiple': '🌐',
        }
        icon = platform_icons.get(obj.platform, '📱')
        return format_html('{} {}', icon, obj.get_platform_display())
    get_platform.short_description = 'Plateforme'
    
    def get_budget(self, obj):
        budget = float(obj.budget) if obj.budget else 0
        return format_html('<span style="color: #FF4500; font-weight: bold;">${:,.2f}</span>', budget)
    get_budget.short_description = 'Budget'
    
    def get_status(self, obj):
        status_colors = {
            'draft': '#6c757d',
            'open': '#28a745',
            'closed': '#dc3545',
            'completed': '#17a2b8',
        }
        color = status_colors.get(obj.status, '#666')
        return format_html('<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold;">{}</span>', color, obj.get_status_display())
    get_status.short_description = 'Statut'

