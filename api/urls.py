from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, ApplicationViewSet, InfluencerProfileViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'influencers', InfluencerProfileViewSet, basename='influencer')

urlpatterns = [
    path('', include(router.urls)),
]
