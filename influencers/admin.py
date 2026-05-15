from django.contrib import admin
from .models import InfluencerProfile


@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'niche', 'location', 'total_followers', 'rate_per_post', 'created_at']
    list_filter = ['niche', 'location', 'created_at']
    search_fields = ['full_name', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at']

