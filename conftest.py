from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        role="influencer",
    )


@pytest.fixture
def test_influencer(db, test_user):
    # Le signal post_save crée automatiquement le profil à la création du user.
    # On récupère ce profil et on le met à jour avec des données de test.
    profile = test_user.influencer_profile
    profile.full_name = "Test Influencer"
    profile.bio = "Test bio"
    profile.niche = "tech"
    profile.instagram_followers = 10000
    profile.location = "Nairobi"
    profile.save()
    return profile


@pytest.fixture
def test_advertiser_user(db):
    return User.objects.create_user(
        username="advertiser",
        email="advertiser@example.com",
        password="testpass123",
        role="advertiser",
    )


@pytest.fixture
def test_advertiser(db, test_advertiser_user):
    # Le signal post_save crée automatiquement le profil à la création du user.
    # On récupère ce profil et on le met à jour avec des données de test.
    profile = test_advertiser_user.advertiser_profile
    profile.company_name = "Test Company"
    profile.industry = "tech"
    profile.description = "Test description"
    profile.location = "Lagos"
    profile.save()
    return profile


@pytest.fixture
def test_campaign(db, test_advertiser):
    from campaigns.models import Campaign

    return Campaign.objects.create(
        advertiser=test_advertiser,
        title="Test Campaign",
        description="Test description",
        requirements="Test requirements",
        budget=1000.00,
        niche="tech",
        platform="instagram",
        deadline="2027-12-31",
        status="open",
    )


@pytest.fixture
def test_application(db, test_influencer, test_campaign):
    from applications.models import Application

    return Application.objects.create(
        campaign=test_campaign,
        influencer=test_influencer,
        pitch="Test pitch",
        proposed_price=500.00,
        status="pending",
    )


@pytest.fixture
def test_currency(db):
    from core.models import Currency

    return Currency.objects.create(
        code="USD",
        name="US Dollar",
        symbol="$",
        exchange_rate_to_usd=1.0,
        is_active=True,
    )


@pytest.fixture
def test_subscription_plan(db, test_currency):
    from core.models import SubscriptionPlan

    return SubscriptionPlan.objects.create(
        name="Pro Test",
        plan_type="pro",
        user_type="influencer",
        price=9.00,
        currency=test_currency,
        commission_rate=15.00,
        is_active=True,
    )
