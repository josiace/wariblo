from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from core.decorators import influencer_required
from .forms import InfluencerProfileForm
from .models import InfluencerProfile
from campaigns.models import Campaign


@influencer_required
def influencer_dashboard(request):
    try:
        profile = request.user.influencer_profile
    except InfluencerProfile.DoesNotExist:
        return redirect('influencer_profile_create')
    
    my_applications = profile.applications.select_related(
        'campaign__advertiser__user'
    ).order_by('-created_at')[:5]
    available_campaigns = Campaign.objects.filter(
        status='open'
    ).select_related('advertiser__user').order_by('-created_at')[:10]
    
    accepted_count = profile.applications.filter(status='accepted').count()
    pending_count = profile.applications.filter(status='pending').count()
    rejected_count = profile.applications.filter(status='rejected').count()
    total_applications = profile.applications.count()
    success_rate = (accepted_count / total_applications * 100) if total_applications > 0 else 0
    
    context = {
        'profile': profile,
        'my_applications': my_applications,
        'available_campaigns': available_campaigns,
        'accepted_count': accepted_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'total_applications': total_applications,
        'success_rate': round(success_rate, 1),
    }
    return render(request, 'influencers/dashboard.html', context)


@influencer_required
def influencer_profile_create(request):
    if hasattr(request.user, 'influencer_profile'):
        return redirect('influencer_dashboard')
    
    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.is_profile_complete = True
            request.user.save()
            return redirect('influencer_dashboard')
    else:
        form = InfluencerProfileForm()
    
    return render(request, 'influencers/profile_form.html', {'form': form})


@influencer_required
def influencer_profile_edit(request):
    profile = get_object_or_404(InfluencerProfile, user=request.user)
    
    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('influencer_dashboard')
    else:
        form = InfluencerProfileForm(instance=profile)
    
    return render(request, 'influencers/profile_form.html', {'form': form})


@influencer_required
def influencer_campaigns(request):
    campaigns = Campaign.objects.filter(
        status='open'
    ).select_related('advertiser__user').order_by('-created_at')
    
    paginator = Paginator(campaigns, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'campaigns': page_obj,
    }
    return render(request, 'influencers/campaigns.html', context)


@influencer_required
def influencer_applications(request):
    try:
        profile = request.user.influencer_profile
        applications = profile.applications.select_related(
            'campaign__advertiser__user'
        ).order_by('-created_at')
    except InfluencerProfile.DoesNotExist:
        return redirect('influencer_profile_create')
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'applications': page_obj,
    }
    return render(request, 'influencers/applications.html', context)


