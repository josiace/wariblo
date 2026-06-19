from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from core.decorators import advertiser_required
from .forms import AdvertiserProfileForm
from .models import AdvertiserProfile
from campaigns.models import Campaign


@advertiser_required
def advertiser_dashboard(request):
    try:
        profile = request.user.advertiser_profile
    except AdvertiserProfile.DoesNotExist:
        return redirect('advertiser_profile_create')
    
    my_campaigns = profile.campaigns.prefetch_related(
        'applications__influencer__user'
    ).order_by('-created_at')[:5]
    open_campaigns_count = profile.campaigns.filter(status='open').count()
    total_campaigns = profile.campaigns.count()
    total_applications = sum(campaign.applications.count() for campaign in profile.campaigns.all())
    accepted_applications = sum(
        campaign.applications.filter(status='accepted').count() 
        for campaign in profile.campaigns.all()
    )
    total_budget = sum(campaign.budget for campaign in profile.campaigns.all())
    
    context = {
        'profile': profile,
        'my_campaigns': my_campaigns,
        'open_campaigns_count': open_campaigns_count,
        'total_campaigns': total_campaigns,
        'total_applications': total_applications,
        'accepted_applications': accepted_applications,
        'total_budget': total_budget,
    }
    return render(request, 'advertisers/dashboard.html', context)


@advertiser_required
def advertiser_profile_create(request):
    if hasattr(request.user, 'advertiser_profile'):
        return redirect('advertiser_dashboard')
    
    if request.method == 'POST':
        form = AdvertiserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.is_profile_complete = True
            request.user.save()
            return redirect('advertiser_dashboard')
    else:
        form = AdvertiserProfileForm()
    
    return render(request, 'advertisers/profile_form.html', {'form': form})


@advertiser_required
def advertiser_profile_edit(request):
    profile = get_object_or_404(AdvertiserProfile, user=request.user)
    
    if request.method == 'POST':
        form = AdvertiserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('advertiser_dashboard')
    else:
        form = AdvertiserProfileForm(instance=profile)
    
    return render(request, 'advertisers/profile_form.html', {'form': form})


@advertiser_required
def advertiser_campaigns(request):
    try:
        profile = request.user.advertiser_profile
        campaigns = profile.campaigns.prefetch_related(
            'applications__influencer__user'
        ).order_by('-created_at')
    except AdvertiserProfile.DoesNotExist:
        return redirect('advertiser_profile_create')
    
    paginator = Paginator(campaigns, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'campaigns': page_obj,
    }
    return render(request, 'advertisers/campaigns.html', context)


