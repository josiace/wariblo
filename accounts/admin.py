from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['get_email', 'username', 'get_role', 'get_country', 'is_profile_complete', 'is_staff', 'created_at']
    list_filter = ['role', 'is_staff', 'is_profile_complete', 'country', 'created_at']
    search_fields = ['email', 'username', 'phone_number']
    ordering = ['-created_at']
    list_per_page = 25
    list_editable = ['is_staff', 'is_profile_complete']
    
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('email', 'username', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'phone_number', 'country')
        }),
        ('Rôle et profil', {
            'fields': ('role', 'is_profile_complete')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined', 'created_at')
        }),
    )
    
    add_fieldsets = (
        ('Informations de connexion', {
            'fields': ('email', 'username', 'password1', 'password2')
        }),
        ('Rôle', {
            'fields': ('role',)
        }),
    )
    
    readonly_fields = ['created_at', 'last_login', 'date_joined']
    
    def get_email(self, obj):
        return format_html('<strong>{}</strong>', obj.email)
    get_email.short_description = 'Email'
    
    def get_role(self, obj):
        role_colors = {
            'influencer': '#FF4500',
            'advertiser': '#FFD700',
            'admin': '#FF1493'
        }
        color = role_colors.get(obj.role, '#666')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_role_display())
    get_role.short_description = 'Rôle'
    
    def get_country(self, obj):
        if obj.country:
            return format_html('{} {}', obj.country.flag_emoji, obj.country.name)
        return '—'
    get_country.short_description = 'Pays'

