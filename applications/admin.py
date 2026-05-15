from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['influencer', 'campaign', 'status', 'proposed_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['influencer__full_name', 'campaign__title']
    readonly_fields = ['created_at', 'updated_at']

