from django.contrib import admin
from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render
import json
from .admin_views import WaribloAdminDashboard


class WaribloAdminSite(admin.AdminSite):
    site_header = 'Wariblo Administration'
    site_title = 'Wariblo Admin'
    index_title = 'Bienvenue sur le panneau d\'administration Wariblo'
    
    def each_context(self, request):
        context = super().each_context(request)
        context['admin_css'] = static(settings.ADMIN_CSS)
        return context
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('analytics/', self.admin_view(self.analytics_view), name='analytics'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Vue du dashboard avec les statistiques"""
        dashboard = WaribloAdminDashboard()
        stats = dashboard.get_stats()
        context = {
            **self.each_context(request),
            'stats': stats,
            'title': 'Dashboard',
        }
        return render(request, 'admin/dashboard.html', context)
    
    def analytics_view(self, request):
        """Vue de l'analyse de données avec les graphiques"""
        dashboard = WaribloAdminDashboard()
        stats = dashboard.get_stats()
        
        # Préparer les données pour les graphiques
        top_influencers_data = []
        for influencer in stats['top_influencers']:
            top_influencers_data.append({
                'full_name': influencer.full_name,
                'total_followers': float(influencer.total_followers) if influencer.total_followers else 0
            })
        
        top_campaigns_data = []
        for campaign in stats['campaigns']['top_campaigns']:
            top_campaigns_data.append({
                'title': campaign.title,
                'budget': float(campaign.budget) if campaign.budget else 0
            })
        
        context = {
            **self.each_context(request),
            'stats': {
                **stats,
                'top_influencers': json.dumps(top_influencers_data),
                'campaigns': {
                    **stats['campaigns'],
                    'top_campaigns': json.dumps(top_campaigns_data)
                }
            },
            'title': 'Analyse de Données',
        }
        return render(request, 'admin/analytics.html', context)


wariblo_admin = WaribloAdminSite(name='wariblo_admin')
