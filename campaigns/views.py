from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from decimal import Decimal
from core.decorators import advertiser_required
from .forms import CampaignForm
from .models import Campaign


def campaign_list(request):
    campaigns = Campaign.objects.filter(
        status='open'
    ).select_related(
        'advertiser__user'
    ).prefetch_related(
        'applications__influencer__user'
    )
    
    # Filtres
    niche_filter = request.GET.get('niche')
    platform_filter = request.GET.get('platform')
    budget_min = request.GET.get('budget_min')
    budget_max = request.GET.get('budget_max')
    q = request.GET.get('q')
    sort = request.GET.get('sort', '-created_at')
    
    # Recommandations personnalisées pour influenceurs connectés
    recommended_campaigns = []
    if request.user.is_authenticated and request.user.is_influencer:
        try:
            from influencers.models import InfluencerProfile
            profile = request.user.influencer_profile
            user_niche = profile.niche
            user_platforms = []
            if profile.instagram_followers > 0:
                user_platforms.append('instagram')
            if profile.tiktok_followers > 0:
                user_platforms.append('tiktok')
            if profile.youtube_subscribers > 0:
                user_platforms.append('youtube')
            
            # Filtrer par niche et plateformes de l'utilisateur
            recommended = campaigns.filter(niche=user_niche)
            if user_platforms:
                recommended = recommended.filter(platform__in=user_platforms)
            recommended_campaigns = list(recommended[:6])
        except InfluencerProfile.DoesNotExist:
            pass
    
    # Recherche par mots-clés
    if q:
        campaigns = campaigns.filter(
            title__icontains=q
        ) | campaigns.filter(
            description__icontains=q
        )
    
    # Filtres existants
    if niche_filter:
        campaigns = campaigns.filter(niche=niche_filter)
    if platform_filter:
        campaigns = campaigns.filter(platform=platform_filter)
    if budget_min:
        campaigns = campaigns.filter(budget__gte=budget_min)
    if budget_max:
        campaigns = campaigns.filter(budget__lte=budget_max)
    
    # Tri
    if sort in ['-created_at', 'created_at', '-budget', 'budget', '-applications_count']:
        campaigns = campaigns.order_by(sort)
    else:
        campaigns = campaigns.order_by('-created_at')
    
    paginator = Paginator(campaigns, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'campaigns': page_obj,
        'niche_filter': niche_filter,
        'platform_filter': platform_filter,
        'budget_min': budget_min,
        'budget_max': budget_max,
        'user': request.user,
        'recommended_campaigns': recommended_campaigns,
    }
    return render(request, 'campaigns/list.html', context)


def campaign_detail(request, pk):
    campaign = get_object_or_404(
        Campaign.objects.select_related('advertiser__user').prefetch_related(
            'applications__influencer__user'
        ),
        pk=pk
    )
    
    has_applied = False
    match_score = 0
    match_details = []
    
    if request.user.is_authenticated and request.user.is_influencer:
        try:
            from influencers.models import InfluencerProfile
            profile = request.user.influencer_profile
            has_applied = campaign.applications.filter(influencer=profile).exists()
            
            # Calculer le score de matching
            score = 0
            details = []
            
            # Matching niche (40 points)
            if profile.niche == campaign.niche:
                score += 40
                details.append(f"✅ Niche: {campaign.niche} correspond à votre profil")
            else:
                details.append(f"❌ Niche: {campaign.niche} différent de votre profil ({profile.niche})")
            
            # Matching plateforme (30 points)
            user_platforms = []
            if profile.instagram_followers > 0:
                user_platforms.append('instagram')
            if profile.tiktok_followers > 0:
                user_platforms.append('tiktok')
            if profile.youtube_subscribers > 0:
                user_platforms.append('youtube')
            
            if campaign.platform in user_platforms:
                score += 30
                details.append(f"✅ Plateforme: {campaign.platform} correspond à vos réseaux")
            elif campaign.platform == 'multiple':
                score += 15
                details.append(f"⚠️ Plateforme: Multiple (vous avez {len(user_platforms)} réseaux)")
            else:
                details.append(f"❌ Plateforme: {campaign.platform} ne correspond pas à vos réseaux")
            
            # Matching budget (30 points)
            if profile.rate_per_post:
                if campaign.budget >= profile.rate_per_post * Decimal('0.8') and campaign.budget <= profile.rate_per_post * Decimal('1.2'):
                    score += 30
                    details.append(f"✅ Budget: Dans votre gamme de prix")
                elif campaign.budget >= profile.rate_per_post * Decimal('0.5'):
                    score += 15
                    details.append(f"⚠️ Budget: Légèrement en dessous de votre prix")
                else:
                    details.append(f"❌ Budget: En dessous de votre prix")
            else:
                details.append(f"⚠️ Budget: Prix non défini dans votre profil")
            
            match_score = score
            match_details = details
        except InfluencerProfile.DoesNotExist:
            pass
    
    breadcrumbs = [
        {'url': '/', 'label': 'Accueil'},
        {'url': '/campaigns/', 'label': 'Campagnes'},
        {'url': None, 'label': campaign.title}
    ]
    
    context = {
        'campaign': campaign,
        'has_applied': has_applied,
        'breadcrumbs': breadcrumbs,
        'match_score': match_score,
        'match_details': match_details,
    }
    return render(request, 'campaigns/detail.html', context)


@advertiser_required
def campaign_create(request):
    try:
        from advertisers.models import AdvertiserProfile
        profile = request.user.advertiser_profile
    except AdvertiserProfile.DoesNotExist:
        return redirect('advertiser_profile_create')
    
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.advertiser = profile
            campaign.save()
            return redirect('campaign_detail', pk=campaign.pk)
    else:
        form = CampaignForm()
    
    return render(request, 'campaigns/form.html', {'form': form})


@advertiser_required
def campaign_edit(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    if campaign.advertiser.user != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_detail', pk=campaign.pk)
    else:
        form = CampaignForm(instance=campaign)
    
    return render(request, 'campaigns/form.html', {'form': form, 'campaign': campaign})


@advertiser_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    if campaign.advertiser.user != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        campaign.delete()
        return redirect('advertiser_campaigns')
    
    return render(request, 'campaigns/delete_confirm.html', {'campaign': campaign})


