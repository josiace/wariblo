import pytest
from django.contrib.auth import get_user_model
from accounts.models import User
from influencers.models import InfluencerProfile
from advertisers.models import AdvertiserProfile
from campaigns.models import Campaign
from applications.models import Application

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='influencer'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'influencer'
        assert user.is_influencer is True
        assert user.is_advertiser is False
    
    def test_user_str(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert str(user) == 'test@example.com'


@pytest.mark.django_db
class TestInfluencerProfile:
    def test_create_influencer_profile(self, test_user):
        profile = InfluencerProfile.objects.create(
            user=test_user,
            full_name='Test Influencer',
            bio='Test bio',
            niche='tech',
            instagram_followers=10000,
            location='Nairobi'
        )
        assert profile.full_name == 'Test Influencer'
        assert profile.niche == 'tech'
        assert profile.total_followers == 10000
    
    def test_influencer_profile_str(self, test_user):
        profile = InfluencerProfile.objects.create(
            user=test_user,
            full_name='Test Influencer',
            bio='Test bio',
            niche='tech',
            instagram_followers=10000,
            location='Nairobi'
        )
        assert str(profile) == 'Test Influencer'


@pytest.mark.django_db
class TestAdvertiserProfile:
    def test_create_advertiser_profile(self, test_advertiser_user):
        profile = AdvertiserProfile.objects.create(
            user=test_advertiser_user,
            company_name='Test Company',
            industry='tech',
            description='Test description',
            location='Lagos'
        )
        assert profile.company_name == 'Test Company'
        assert profile.industry == 'tech'
    
    def test_advertiser_profile_str(self, test_advertiser_user):
        profile = AdvertiserProfile.objects.create(
            user=test_advertiser_user,
            company_name='Test Company',
            industry='tech',
            description='Test description',
            location='Lagos'
        )
        assert str(profile) == 'Test Company'


@pytest.mark.django_db
class TestCampaign:
    def test_create_campaign(self, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title='Test Campaign',
            description='Test description',
            requirements='Test requirements',
            budget=1000.00,
            niche='tech',
            platform='instagram',
            deadline='2026-12-31',
            status='open'
        )
        assert campaign.title == 'Test Campaign'
        assert campaign.budget == 1000.00
        assert campaign.is_open is True
    
    def test_campaign_str(self, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title='Test Campaign',
            description='Test description',
            requirements='Test requirements',
            budget=1000.00,
            niche='tech',
            platform='instagram',
            deadline='2026-12-31',
            status='open'
        )
        assert str(campaign) == 'Test Campaign'


@pytest.mark.django_db
class TestApplication:
    def test_create_application(self, test_influencer, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title='Test Campaign',
            description='Test description',
            requirements='Test requirements',
            budget=1000.00,
            niche='tech',
            platform='instagram',
            deadline='2026-12-31',
            status='open'
        )
        application = Application.objects.create(
            campaign=campaign,
            influencer=test_influencer,
            pitch='Test pitch',
            proposed_price=500.00,
            status='pending'
        )
        assert application.pitch == 'Test pitch'
        assert application.is_pending is True
    
    def test_application_unique_constraint(self, test_influencer, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title='Test Campaign',
            description='Test description',
            requirements='Test requirements',
            budget=1000.00,
            niche='tech',
            platform='instagram',
            deadline='2026-12-31',
            status='open'
        )
        Application.objects.create(
            campaign=campaign,
            influencer=test_influencer,
            pitch='Test pitch',
            proposed_price=500.00,
            status='pending'
        )
        with pytest.raises(Exception):
            Application.objects.create(
                campaign=campaign,
                influencer=test_influencer,
                pitch='Test pitch 2',
                proposed_price=600.00,
                status='pending'
            )
