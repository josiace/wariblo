from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import influencer_required, advertiser_required
from .forms import ApplicationForm
from .models import Application
from campaigns.models import Campaign
from influencers.models import InfluencerProfile


@influencer_required
def application_create(request, campaign_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    
    try:
        profile = request.user.influencer_profile
    except InfluencerProfile.DoesNotExist:
        return redirect('influencer_profile_create')
    
    if Application.objects.filter(campaign=campaign, influencer=profile).exists():
        messages.warning(request, 'Vous avez déjà postulé à cette campagne.')
        return redirect('campaign_detail', pk=campaign.pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.campaign = campaign
            application.influencer = profile
            application.save()
            messages.success(request, 'Candidature soumise avec succès!')
            return redirect('influencer_applications')
    else:
        form = ApplicationForm()
    
    context = {
        'form': form,
        'campaign': campaign,
    }
    return render(request, 'applications/form.html', context)


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if request.user.is_influencer:
        if application.influencer.user != request.user:
            return redirect('dashboard')
    elif request.user.is_advertiser:
        if application.campaign.advertiser.user != request.user:
            return redirect('dashboard')
    else:
        return redirect('dashboard')
    
    context = {
        'application': application,
    }
    return render(request, 'applications/detail.html', context)


@advertiser_required
def application_accept(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if application.campaign.advertiser.user != request.user:
        return redirect('dashboard')
    
    if application.status == 'pending':
        application.status = 'accepted'
        application.save()
        messages.success(request, 'Candidature acceptée!')
    
    return redirect('campaign_applications', campaign_pk=application.campaign.pk)


@advertiser_required
def application_reject(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if application.campaign.advertiser.user != request.user:
        return redirect('dashboard')
    
    if application.status == 'pending':
        application.status = 'rejected'
        application.save()
        messages.success(request, 'Candidature rejetée.')
    
    return redirect('campaign_applications', campaign_pk=application.campaign.pk)


@influencer_required
def application_withdraw(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if application.influencer.user != request.user:
        return redirect('dashboard')
    
    if application.status == 'pending':
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Candidature retirée.')
    
    return redirect('influencer_applications')


@advertiser_required
def campaign_applications(request, campaign_pk):
    campaign = get_object_or_404(
        Campaign.objects.select_related('advertiser__user'),
        pk=campaign_pk
    )
    
    if campaign.advertiser.user != request.user:
        return redirect('dashboard')
    
    applications = campaign.applications.select_related(
        'influencer__user'
    ).order_by('-created_at')
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'campaign': campaign,
        'page_obj': page_obj,
        'applications': page_obj,
    }
    return render(request, 'applications/campaign_applications.html', context)


