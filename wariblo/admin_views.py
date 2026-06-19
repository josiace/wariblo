from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from accounts.models import User as CustomUser
from influencers.models import InfluencerProfile
from advertisers.models import AdvertiserProfile
from campaigns.models import Campaign
from applications.models import Application
from messaging.models import Conversation, Message
from core.models import Country
import json


class WaribloAdminDashboard(admin.ModelAdmin):
    """Dashboard admin avec graphiques et statistiques"""
    
    def get_stats(self):
        """Récupérer les statistiques pour le dashboard"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        last_7_days = now - timedelta(days=7)
        
        # Statistiques utilisateurs
        total_users = CustomUser.objects.count()
        influencers_count = CustomUser.objects.filter(role='influencer').count()
        advertisers_count = CustomUser.objects.filter(role='advertiser').count()
        admins_count = CustomUser.objects.filter(role='admin').count()
        
        # Statistiques campagnes
        total_campaigns = Campaign.objects.count()
        open_campaigns = Campaign.objects.filter(status='open').count()
        closed_campaigns = Campaign.objects.filter(status='closed').count()
        total_budget = Campaign.objects.aggregate(Sum('budget'))['budget__sum'] or 0
        
        # Statistiques applications
        total_applications = Application.objects.count()
        pending_applications = Application.objects.filter(status='pending').count()
        accepted_applications = Application.objects.filter(status='accepted').count()
        rejected_applications = Application.objects.filter(status='rejected').count()
        
        # Statistiques messaging
        total_conversations = Conversation.objects.count()
        total_messages = Message.objects.count()
        
        # Statistiques pays
        total_countries = Country.objects.count()
        active_countries = Country.objects.filter(is_active=True).count()
        
        # Données pour les graphiques
        # Campagnes par statut
        campaigns_by_status = list(Campaign.objects.values('status').annotate(count=Count('id')).order_by('status'))
        
        # Applications par statut
        applications_by_status = list(Application.objects.values('status').annotate(count=Count('id')).order_by('status'))
        
        # Utilisateurs par rôle
        users_by_role = list(CustomUser.objects.values('role').annotate(count=Count('id')).order_by('role'))
        
        # Campagnes créées par mois (derniers 6 mois)
        campaigns_by_month = []
        for i in range(6):
            month_start = now - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            count = Campaign.objects.filter(created_at__range=[month_start, month_end]).count()
            campaigns_by_month.append({
                'month': month_start.strftime('%b'),
                'count': count
            })
        campaigns_by_month.reverse()
        
        # Applications par mois (derniers 6 mois)
        applications_by_month = []
        for i in range(6):
            month_start = now - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            count = Application.objects.filter(created_at__range=[month_start, month_end]).count()
            applications_by_month.append({
                'month': month_start.strftime('%b'),
                'count': count
            })
        applications_by_month.reverse()
        
        # Top 5 influenceurs par followers
        top_influencers = list(InfluencerProfile.objects.order_by('-total_followers')[:5])
        
        # Top 5 campagnes par budget
        top_campaigns = list(Campaign.objects.order_by('-budget')[:5])
        
        return {
            'users': {
                'total': total_users,
                'influencers': influencers_count,
                'advertisers': advertisers_count,
                'admins': admins_count,
                'by_role': json.dumps(users_by_role),
            },
            'campaigns': {
                'total': total_campaigns,
                'open': open_campaigns,
                'closed': closed_campaigns,
                'total_budget': float(total_budget),
                'by_status': json.dumps(campaigns_by_status),
                'by_month': json.dumps(campaigns_by_month),
                'top_campaigns': top_campaigns,
            },
            'applications': {
                'total': total_applications,
                'pending': pending_applications,
                'accepted': accepted_applications,
                'rejected': rejected_applications,
                'by_status': json.dumps(applications_by_status),
                'by_month': json.dumps(applications_by_month),
            },
            'messaging': {
                'total_conversations': total_conversations,
                'total_messages': total_messages,
            },
            'countries': {
                'total': total_countries,
                'active': active_countries,
            },
            'top_influencers': top_influencers,
        }
