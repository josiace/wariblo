import pytest
from django.contrib.auth import get_user_model

from accounts.models import User
from advertisers.models import AdvertiserProfile
from applications.models import Application
from campaigns.models import Campaign
from influencers.models import InfluencerProfile

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            username="newuser",
            email="new@example.com",
            password="testpass123",
            role="influencer",
        )
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.role == "influencer"
        assert user.is_influencer is True
        assert user.is_advertiser is False

    def test_user_str(self):
        user = User.objects.create_user(
            username="struser", email="str@example.com", password="testpass123"
        )
        assert str(user) == "str@example.com"

    def test_is_admin_user(self):
        user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="testpass123",
            role="admin",
        )
        assert user.is_admin_user is True

    def test_superuser_is_admin(self):
        user = User.objects.create_superuser(
            username="superuser", email="super@example.com", password="testpass123"
        )
        assert user.is_admin_user is True


@pytest.mark.django_db
class TestInfluencerProfile:
    def test_create_influencer_profile(self, test_user):
        # Le signal post_save crée automatiquement un profil vide.
        # On le met à jour avec des valeurs de test.
        profile = test_user.influencer_profile
        profile.full_name = "Test Influencer"
        profile.bio = "Test bio"
        profile.niche = "tech"
        profile.instagram_followers = 10000
        profile.location = "Nairobi"
        profile.save()
        profile.refresh_from_db()
        assert profile.full_name == "Test Influencer"
        assert profile.niche == "tech"
        assert profile.total_followers == 10000

    def test_influencer_profile_str(self, test_influencer):
        assert str(test_influencer) == "Test Influencer"

    def test_total_followers_sum(self, test_user):
        profile = test_user.influencer_profile
        profile.instagram_followers = 5000
        profile.tiktok_followers = 3000
        profile.youtube_subscribers = 1000
        profile.twitter_followers = 500
        profile.save()
        assert profile.total_followers == 9500


@pytest.mark.django_db
class TestAdvertiserProfile:
    def test_create_advertiser_profile(self, test_advertiser_user):
        # Le signal post_save crée automatiquement un profil vide.
        profile = test_advertiser_user.advertiser_profile
        profile.company_name = "My Company"
        profile.industry = "tech"
        profile.description = "Test description"
        profile.location = "Lagos"
        profile.save()
        profile.refresh_from_db()
        assert profile.company_name == "My Company"
        assert profile.industry == "tech"

    def test_advertiser_profile_str(self, test_advertiser):
        assert str(test_advertiser) == "Test Company"


@pytest.mark.django_db
class TestCampaign:
    def test_create_campaign(self, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title="Test Campaign",
            description="Test description",
            requirements="Test requirements",
            budget=1000.00,
            niche="tech",
            platform="instagram",
            deadline="2026-12-31",
            status="open",
        )
        assert campaign.title == "Test Campaign"
        assert campaign.budget == 1000.00
        assert campaign.is_open is True

    def test_campaign_str(self, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title="Test Campaign",
            description="Test description",
            requirements="Test requirements",
            budget=1000.00,
            niche="tech",
            platform="instagram",
            deadline="2026-12-31",
            status="open",
        )
        assert str(campaign) == "Test Campaign"

    def test_campaign_not_open_when_draft(self, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title="Draft Campaign",
            description="Test",
            requirements="Test",
            budget=500.00,
            niche="fashion",
            platform="tiktok",
            deadline="2026-12-31",
            status="draft",
        )
        assert campaign.is_open is False

    def test_applications_count(self, test_campaign, test_application):
        assert test_campaign.applications_count == 1


@pytest.mark.django_db
class TestApplication:
    def test_create_application(self, test_influencer, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title="Test Campaign",
            description="Test description",
            requirements="Test requirements",
            budget=1000.00,
            niche="tech",
            platform="instagram",
            deadline="2026-12-31",
            status="open",
        )
        application = Application.objects.create(
            campaign=campaign,
            influencer=test_influencer,
            pitch="Test pitch",
            proposed_price=500.00,
            status="pending",
        )
        assert application.pitch == "Test pitch"
        assert application.is_pending is True
        assert application.is_accepted is False
        assert application.is_rejected is False

    def test_application_unique_constraint(self, test_influencer, test_advertiser):
        campaign = Campaign.objects.create(
            advertiser=test_advertiser,
            title="Test Campaign",
            description="Test description",
            requirements="Test requirements",
            budget=1000.00,
            niche="tech",
            platform="instagram",
            deadline="2026-12-31",
            status="open",
        )
        Application.objects.create(
            campaign=campaign,
            influencer=test_influencer,
            pitch="Test pitch",
            proposed_price=500.00,
            status="pending",
        )
        with pytest.raises(Exception):
            Application.objects.create(
                campaign=campaign,
                influencer=test_influencer,
                pitch="Test pitch 2",
                proposed_price=600.00,
                status="pending",
            )

    def test_application_status_transitions(self, test_application):
        test_application.status = "accepted"
        test_application.save()
        test_application.refresh_from_db()
        assert test_application.is_accepted is True
        assert test_application.is_pending is False

        test_application.status = "rejected"
        test_application.save()
        test_application.refresh_from_db()
        assert test_application.is_rejected is True


@pytest.mark.django_db
class TestCurrencyModel:
    def test_currency_str(self, test_currency):
        assert "$ USD" in str(test_currency)

    def test_convert_to_usd(self, test_currency):
        # USD to USD (rate=1.0)
        assert test_currency.convert_to_usd(100) == 100.0

    def test_convert_from_usd(self, db):
        from core.models import Currency

        # XOF : 1 USD = 600 XOF → exchange_rate_to_usd = 1/600
        xof = Currency.objects.create(
            code="XOF",
            name="Franc CFA",
            symbol="CFA",
            exchange_rate_to_usd=1 / 600,
        )
        result = xof.convert_to_usd(600)
        assert abs(result - 1.0) < 0.01
