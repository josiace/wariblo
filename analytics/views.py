from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Sum
from .models import CampaignAnalytics, UserActivity
from campaigns.models import Campaign


@login_required
def campaign_analytics_dashboard(request):
    """Tableau de bord des analytics de campagnes pour l'annonceur"""
    if request.user.is_advertiser:
        from advertisers.models import AdvertiserProfile
        try:
            profile = request.user.advertiser_profile
            campaigns = profile.campaigns.all()
        except AdvertiserProfile.DoesNotExist:
            campaigns = Campaign.objects.none()
    else:
        campaigns = Campaign.objects.none()
    
    # Récupérer les analytics pour chaque campagne
    campaigns_with_analytics = []
    for campaign in campaigns:
        try:
            analytics = campaign.analytics
            campaigns_with_analytics.append({
                'campaign': campaign,
                'analytics': analytics,
            })
        except CampaignAnalytics.DoesNotExist:
            # Créer des analytics par défaut si n'existent pas
            analytics = CampaignAnalytics.objects.create(campaign=campaign)
            campaigns_with_analytics.append({
                'campaign': campaign,
                'analytics': analytics,
            })
    
    # Statistiques globales
    total_views = sum(c['analytics'].total_views for c in campaigns_with_analytics)
    total_clicks = sum(c['analytics'].total_clicks for c in campaigns_with_analytics)
    total_shares = sum(c['analytics'].total_shares for c in campaigns_with_analytics)
    
    context = {
        'campaigns_with_analytics': campaigns_with_analytics,
        'total_views': total_views,
        'total_clicks': total_clicks,
        'total_shares': total_shares,
    }
    return render(request, 'analytics/campaign_dashboard.html', context)


@login_required
def campaign_analytics_detail(request, campaign_id):
    """Détails des analytics pour une campagne spécifique"""
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    
    # Vérifier que l'utilisateur a le droit de voir ces analytics
    if request.user.is_advertiser:
        if campaign.advertiser.user != request.user:
            from django.contrib import messages
            messages.error(request, "Vous n'avez pas le droit de voir ces analytics.")
            return redirect('analytics:campaign_dashboard')
    
    try:
        analytics = campaign.analytics
    except CampaignAnalytics.DoesNotExist:
        analytics = CampaignAnalytics.objects.create(campaign=campaign)
    
    # Activités des utilisateurs sur cette campagne
    activities = UserActivity.objects.filter(
        campaign=campaign
    ).select_related('user').order_by('-created_at')[:50]
    
    # Statistiques par type d'activité
    activity_stats = UserActivity.objects.filter(
        campaign=campaign
    ).values('activity_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'campaign': campaign,
        'analytics': analytics,
        'activities': activities,
        'activity_stats': activity_stats,
    }
    return render(request, 'analytics/campaign_detail.html', context)


@login_required
def user_activity_dashboard(request):
    """Tableau de bord des activités de l'utilisateur"""
    if request.user.is_influencer:
        # Pour les influenceurs, montrer leurs activités sur les campagnes
        activities = UserActivity.objects.filter(
            user=request.user
        ).select_related('campaign').order_by('-created_at')
    elif request.user.is_advertiser:
        # Pour les annonceurs, montrer les activités sur leurs campagnes
        from advertisers.models import AdvertiserProfile
        try:
            profile = request.user.advertiser_profile
            campaign_ids = profile.campaigns.values_list('id', flat=True)
            activities = UserActivity.objects.filter(
                campaign_id__in=campaign_ids
            ).select_related('user', 'campaign').order_by('-created_at')
        except AdvertiserProfile.DoesNotExist:
            activities = UserActivity.objects.none()
    else:
        activities = UserActivity.objects.none()
    
    # Statistiques par type d'activité
    activity_stats = activities.values('activity_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    paginator = Paginator(activities, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'activities': page_obj,
        'activity_stats': activity_stats,
    }
    return render(request, 'analytics/user_activity.html', context)
