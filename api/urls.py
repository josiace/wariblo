from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CampaignViewSet, ApplicationViewSet, InfluencerProfileViewSet,
    AdvertiserProfileViewSet, UserViewSet, ConversationViewSet,
    MessageViewSet, ReviewViewSet, CampaignAnalyticsViewSet,
    UserActivityViewSet, CountryViewSet, CurrencyViewSet,
    SubscriptionPlanViewSet, SubscriptionViewSet, TransactionViewSet,
    PaymentMethodViewSet, ManualPaymentViewSet, SiteSettingsViewSet,
    register, login, logout
)

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'influencers', InfluencerProfileViewSet, basename='influencer')
router.register(r'advertisers', AdvertiserProfileViewSet, basename='advertiser')
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'campaign-analytics', CampaignAnalyticsViewSet, basename='campaign-analytics')
router.register(r'user-activities', UserActivityViewSet, basename='user-activity')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscription-plan')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-method')
router.register(r'manual-payments', ManualPaymentViewSet, basename='manual-payment')
router.register(r'site-settings', SiteSettingsViewSet, basename='site-settings')

urlpatterns = [
    path('auth/register/', register, name='api-register'),
    path('auth/login/', login, name='api-login'),
    path('auth/logout/', logout, name='api-logout'),
    path('', include(router.urls)),
]
