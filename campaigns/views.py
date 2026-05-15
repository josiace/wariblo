from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from core.decorators import advertiser_required
from .forms import CampaignForm
from .models import Campaign


def campaign_list(request):
    campaigns = Campaign.objects.filter(status='open').order_by('-created_at')
    
    niche_filter = request.GET.get('niche')
    platform_filter = request.GET.get('platform')
    
    if niche_filter:
        campaigns = campaigns.filter(niche__icontains=niche_filter)
    if platform_filter:
        campaigns = campaigns.filter(platform=platform_filter)
    
    paginator = Paginator(campaigns, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'campaigns': page_obj,
        'niche_filter': niche_filter,
        'platform_filter': platform_filter,
    }
    return render(request, 'campaigns/list.html', context)


def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    has_applied = False
    if request.user.is_authenticated and request.user.is_influencer:
        try:
            from influencers.models import InfluencerProfile
            profile = request.user.influencer_profile
            has_applied = campaign.applications.filter(influencer=profile).exists()
        except InfluencerProfile.DoesNotExist:
            pass
    
    context = {
        'campaign': campaign,
        'has_applied': has_applied,
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


