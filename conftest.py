import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        role='influencer'
    )


@pytest.fixture
def test_influencer(db, test_user):
    from influencers.models import InfluencerProfile
    return InfluencerProfile.objects.create(
        user=test_user,
        full_name='Test Influencer',
        bio='Test bio',
        niche='tech',
        instagram_followers=10000,
        location='Nairobi'
    )


@pytest.fixture
def test_advertiser_user(db):
    return User.objects.create_user(
        username='advertiser',
        email='advertiser@example.com',
        password='testpass123',
        role='advertiser'
    )


@pytest.fixture
def test_advertiser(db, test_advertiser_user):
    from advertisers.models import AdvertiserProfile
    return AdvertiserProfile.objects.create(
        user=test_advertiser_user,
        company_name='Test Company',
        industry='tech',
        description='Test description',
        location='Lagos'
    )
