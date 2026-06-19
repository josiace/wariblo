from django.contrib import admin
from django.utils.html import format_html
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_influencer', 'get_campaign', 'get_status', 'get_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['influencer__full_name', 'campaign__title', 'pitch']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    ordering = ['-created_at']
    
    fieldsets = (
        ('Candidature', {
            'fields': ('campaign', 'influencer', 'status')
        }),
        ('Détails', {
            'fields': ('pitch', 'proposed_price')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_influencer(self, obj):
        return format_html('<strong>{}</strong>', obj.influencer.full_name)
    get_influencer.short_description = 'Influenceur'
    
    def get_campaign(self, obj):
        return obj.campaign.title if obj.campaign else '—'
    get_campaign.short_description = 'Campagne'
    
    def get_status(self, obj):
        status_colors = {
            'pending': '#FFD700',
            'accepted': '#28a745',
            'rejected': '#dc3545',
            'withdrawn': '#6c757d',
        }
        color = status_colors.get(obj.status, '#666')
        return format_html('<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold;">{}</span>', color, obj.get_status_display())
    get_status.short_description = 'Statut'
    
    def get_price(self, obj):
        if obj.proposed_price:
            price = float(obj.proposed_price)
            return format_html('<span style="color: #FF4500; font-weight: bold;">${:.2f}</span>', price)
        return '—'
    get_price.short_description = 'Prix proposé'

