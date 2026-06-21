from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from decimal import Decimal

from core.models import Subscription, SubscriptionPlan, Transaction
from campaigns.models import Campaign
from core.decorators import advertiser_required, influencer_required
from core.models import Currency
from influencers.models import InfluencerProfile

from .forms import ApplicationForm
from .models import Application


@influencer_required
def application_create(request, campaign_pk):
    campaign = get_object_or_404(Campaign, pk=campaign_pk)

    try:
        profile = request.user.influencer_profile
    except InfluencerProfile.DoesNotExist:
        return redirect("influencer_profile_create")

    if Application.objects.filter(campaign=campaign, influencer=profile).exists():
        messages.warning(request, "Vous avez déjà postulé à cette campagne.")
        return redirect("campaign_detail", pk=campaign.pk)

    # Calculer la suggestion de prix
    suggested_price = None
    price_min = None
    price_max = None

    if profile.rate_per_post:
        suggested_price = profile.rate_per_post
        price_min = profile.rate_per_post * Decimal('0.8')
        price_max = profile.rate_per_post * Decimal('1.2')

    # Ajuster selon le budget de la campagne
    if campaign.budget and suggested_price:
        if suggested_price > campaign.budget:
            suggested_price = campaign.budget * Decimal('0.9')
            price_min = campaign.budget * Decimal('0.7')
            price_max = campaign.budget

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.campaign = campaign
            application.influencer = profile
            application.save()
            messages.success(request, "Candidature soumise avec succès!")
            return redirect("influencer_applications")
    else:
        form = ApplicationForm()
        if suggested_price:
            form.fields["proposed_price"].initial = suggested_price

    context = {
        "form": form,
        "campaign": campaign,
        "suggested_price": suggested_price,
        "price_min": price_min,
        "price_max": price_max,
    }
    return render(request, "applications/form.html", context)


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.user.is_influencer:
        if application.influencer.user != request.user:
            return redirect("dashboard")
    elif request.user.is_advertiser:
        if application.campaign.advertiser.user != request.user:
            return redirect("dashboard")
    else:
        return redirect("dashboard")

    context = {
        "application": application,
    }
    return render(request, "applications/detail.html", context)


@advertiser_required
def application_accept(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if application.campaign.advertiser.user != request.user:
        return redirect("dashboard")

    if application.status == "pending":
        application.status = "accepted"
        application.save()

        # Créer une transaction de commission
        # Obtenir le plan d'abonnement de l'annonceur
        advertiser_subscription = Subscription.objects.filter(
            user=application.campaign.advertiser.user,
            status="active",
            end_date__gt=timezone.now(),
        ).first()

        # Déterminer le taux de commission
        if advertiser_subscription:
            commission_rate = advertiser_subscription.plan.commission_rate
        else:
            # Utiliser le taux par défaut du plan gratuit
            commission_rate = 20.00

        # Calculer le montant de la commission
        commission_amount = application.proposed_price * (commission_rate / 100)

        # Obtenir ou créer la devise USD
        usd, _ = Currency.objects.get_or_create(
            code="USD",
            defaults={
                "name": "US Dollar",
                "symbol": "$",
                "exchange_rate_to_usd": 1.0,
                "is_active": True,
            },
        )

        # Créer la transaction
        Transaction.objects.create(
            user=application.campaign.advertiser.user,
            transaction_type="commission",
            status="pending",
            amount=commission_amount,
            currency=usd,
            campaign=application.campaign,
            application=application,
            commission_rate=commission_rate,
            commission_amount=commission_amount,
            description=f"Commission pour acceptation de candidature - {application.campaign.title}",
            payment_id=f"COMM-{application.id}-{application.campaign.id}",
        )

        messages.success(
            request,
            "Candidature acceptée! Une commission de {} {} a été générée.".format(
                commission_amount, usd.symbol
            ),
        )

    return redirect("campaign_applications", campaign_pk=application.campaign.pk)


@advertiser_required
def application_reject(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if application.campaign.advertiser.user != request.user:
        return redirect("dashboard")

    if application.status == "pending":
        application.status = "rejected"
        application.save()
        messages.success(request, "Candidature rejetée.")

    return redirect("campaign_applications", campaign_pk=application.campaign.pk)


@influencer_required
def application_withdraw(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if application.influencer.user != request.user:
        return redirect("dashboard")

    if application.status == "pending":
        application.status = "withdrawn"
        application.save()
        messages.success(request, "Candidature retirée.")

    return redirect("influencer_applications")


@advertiser_required
def campaign_applications(request, campaign_pk):
    campaign = get_object_or_404(
        Campaign.objects.select_related("advertiser__user"), pk=campaign_pk
    )

    if campaign.advertiser.user != request.user:
        return redirect("dashboard")

    applications = campaign.applications.select_related("influencer__user").order_by(
        "-created_at"
    )

    paginator = Paginator(applications, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "campaign": campaign,
        "page_obj": page_obj,
        "applications": page_obj,
    }
    return render(request, "applications/campaign_applications.html", context)
