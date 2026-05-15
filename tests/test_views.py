import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestCoreViews:
    def test_landing_page(self, client):
        response = client.get(reverse('landing'))
        assert response.status_code == 200
    
    def test_about_page(self, client):
        response = client.get(reverse('about'))
        assert response.status_code == 200
    
    def test_contact_page(self, client):
        response = client.get(reverse('contact'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestAuthViews:
    def test_login_page(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_register_page(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200
    
    def test_user_registration(self, client):
        response = client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'role': 'influencer',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        assert response.status_code == 302
        assert User.objects.filter(email='newuser@example.com').exists()
    
    def test_user_login(self, client, test_user):
        response = client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        assert response.status_code == 302


@pytest.mark.django_db
class TestInfluencerViews:
    def test_influencer_dashboard_requires_login(self, client):
        response = client.get(reverse('influencer_dashboard'))
        assert response.status_code == 302
    
    def test_influencer_dashboard_authenticated(self, client, test_influencer):
        client.force_login(test_influencer.user)
        response = client.get(reverse('influencer_dashboard'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestAdvertiserViews:
    def test_advertiser_dashboard_requires_login(self, client):
        response = client.get(reverse('advertiser_dashboard'))
        assert response.status_code == 302
    
    def test_advertiser_dashboard_authenticated(self, client, test_advertiser):
        client.force_login(test_advertiser.user)
        response = client.get(reverse('advertiser_dashboard'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestCampaignViews:
    def test_campaign_list(self, client):
        response = client.get(reverse('campaign_list'))
        assert response.status_code == 200
    
    def test_campaign_detail(self, client, test_advertiser):
        from campaigns.models import Campaign
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
        response = client.get(reverse('campaign_detail', kwargs={'pk': campaign.pk}))
        assert response.status_code == 200
