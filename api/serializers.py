from rest_framework import serializers
from campaigns.models import Campaign
from applications.models import Application
from influencers.models import InfluencerProfile
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'phone_number', 'country', 'created_at']
        read_only_fields = ['id', 'created_at']


class InfluencerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_followers = serializers.ReadOnlyField()
    
    class Meta:
        model = InfluencerProfile
        fields = ['id', 'user', 'full_name', 'bio', 'niche', 'instagram_followers', 
                  'tiktok_followers', 'youtube_subscribers', 'twitter_followers', 
                  'rate_per_post', 'profile_image', 'location', 'total_followers', 'created_at']
        read_only_fields = ['id', 'created_at']


class CampaignSerializer(serializers.ModelSerializer):
    advertiser = InfluencerProfileSerializer(read_only=True)
    applications_count = serializers.ReadOnlyField()
    is_open = serializers.ReadOnlyField()
    
    class Meta:
        model = Campaign
        fields = ['id', 'advertiser', 'title', 'description', 'requirements', 'budget', 
                  'niche', 'platform', 'deadline', 'status', 'applications_count', 'is_open', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicationSerializer(serializers.ModelSerializer):
    influencer = InfluencerProfileSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)
    is_pending = serializers.ReadOnlyField()
    is_accepted = serializers.ReadOnlyField()
    is_rejected = serializers.ReadOnlyField()
    
    class Meta:
        model = Application
        fields = ['id', 'campaign', 'influencer', 'pitch', 'proposed_price', 'status', 
                  'is_pending', 'is_accepted', 'is_rejected', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['campaign', 'pitch', 'proposed_price']
