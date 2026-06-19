from django.contrib import admin
from .models import CampaignAnalytics, UserActivity


@admin.register(CampaignAnalytics)
class CampaignAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'total_views', 'unique_views', 'total_clicks', 'conversion_rate', 'roi', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['campaign__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Campagne', {
            'fields': ('campaign',)
        }),
        ('Statistiques de vues', {
            'fields': ('total_views', 'unique_views')
        }),
        ('Statistiques d\'engagement', {
            'fields': ('total_clicks', 'total_shares', 'engagement_rate')
        }),
        ('Statistiques de conversion', {
            'fields': ('conversion_rate', 'roi')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'campaign', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__email', 'campaign__title']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Activité', {
            'fields': ('activity_type', 'campaign', 'metadata')
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
