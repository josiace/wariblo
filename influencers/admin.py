from django.contrib import admin
from django.utils.html import format_html
from .models import InfluencerProfile


@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_email', 'get_niche', 'location', 'get_followers', 'get_rate', 'created_at']
    list_filter = ['niche', 'location', 'created_at']
    search_fields = ['full_name', 'user__email', 'location']
    readonly_fields = ['total_followers', 'created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user', 'full_name')
        }),
        ('Profil influenceur', {
            'fields': ('niche', 'bio', 'location')
        }),
        ('Statistiques réseaux sociaux', {
            'fields': ('instagram_followers', 'tiktok_followers', 'youtube_subscribers', 'twitter_followers', 'total_followers')
        }),
        ('Tarification', {
            'fields': ('rate_per_post',)
        }),
        ('Image', {
            'fields': ('profile_image',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_name(self, obj):
        return format_html('<strong>{}</strong>', obj.full_name)
    get_name.short_description = 'Nom complet'
    
    def get_email(self, obj):
        return obj.user.email if obj.user else '—'
    get_email.short_description = 'Email'
    
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
        }
        color = niche_colors.get(obj.niche, '#666')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_niche_display())
    get_niche.short_description = 'Niche'
    
    def get_followers(self, obj):
        followers = float(obj.total_followers) if obj.total_followers else 0
        if followers > 1000000:
            return format_html('<span style="color: #FF4500; font-weight: bold;">{:.1f}M</span>', followers / 1000000)
        elif followers > 1000:
            return format_html('<span style="color: #FFD700; font-weight: bold;">{:.1f}K</span>', followers / 1000)
        return format_html('<span>{}</span>', int(followers))
    get_followers.short_description = 'Total followers'
    
    def get_rate(self, obj):
        if obj.rate_per_post:
            rate = float(obj.rate_per_post)
            return format_html('<span style="color: #FF4500; font-weight: bold;">${:,.2f}</span>', rate)
        return '—'
    get_rate.short_description = 'Tarif/post'

