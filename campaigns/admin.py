from django.contrib import admin
from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'advertiser', 'niche', 'platform', 'budget', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'platform', 'niche', 'created_at']
    search_fields = ['title', 'advertiser__company_name', 'description']
    readonly_fields = ['created_at', 'updated_at']

