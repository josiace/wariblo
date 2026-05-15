from django.contrib import admin
from .models import AdvertiserProfile


@admin.register(AdvertiserProfile)
class AdvertiserProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'industry', 'location', 'created_at']
    list_filter = ['industry', 'location', 'created_at']
    search_fields = ['company_name', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at']

