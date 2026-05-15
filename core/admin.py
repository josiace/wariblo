from django.contrib import admin
from .models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'phone_code', 'flag_emoji', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'phone_code']
    list_editable = ['is_active']

