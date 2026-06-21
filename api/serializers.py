from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from campaigns.models import Campaign
from applications.models import Application
from influencers.models import InfluencerProfile
from advertisers.models import AdvertiserProfile
from accounts.models import User
from messaging.models import Conversation, Message
from reviews.models import Review
from analytics.models import CampaignAnalytics, UserActivity
from core.models import Country, Currency, SubscriptionPlan, Subscription, Transaction, PaymentMethod, ManualPayment, SiteSettings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'phone_number', 'country', 'is_profile_complete', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'role', 'phone_number', 'country']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Email ou mot de passe incorrect.')
            if not user.is_active:
                raise serializers.ValidationError('Ce compte est désactivé.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email et mot de passe requis.')
        
        return attrs


class InfluencerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_followers = serializers.ReadOnlyField()
    
    class Meta:
        model = InfluencerProfile
        fields = ['id', 'user', 'full_name', 'bio', 'niche', 'instagram_followers', 
                  'tiktok_followers', 'youtube_subscribers', 'twitter_followers', 
                  'rate_per_post', 'profile_image', 'location', 'total_followers', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class InfluencerProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfluencerProfile
        fields = ['full_name', 'bio', 'niche', 'instagram_followers', 'tiktok_followers',
                  'youtube_subscribers', 'twitter_followers', 'rate_per_post', 'profile_image', 'location']


class AdvertiserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AdvertiserProfile
        fields = ['id', 'user', 'company_name', 'industry', 'company_description', 
                  'company_logo', 'location', 'website', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdvertiserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserProfile
        fields = ['company_name', 'industry', 'company_description', 'company_logo', 'location', 'website']


class CampaignSerializer(serializers.ModelSerializer):
    advertiser = AdvertiserProfileSerializer(read_only=True)
    applications_count = serializers.ReadOnlyField()
    is_open = serializers.ReadOnlyField()
    
    class Meta:
        model = Campaign
        fields = ['id', 'advertiser', 'title', 'description', 'requirements', 'budget', 
                  'niche', 'platform', 'deadline', 'status', 'applications_count', 'is_open', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CampaignCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'requirements', 'budget', 'niche', 'platform', 'deadline']


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


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message', 'last_message_preview', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_last_message_preview(self, obj):
        if obj.last_message:
            return obj.last_message.content[:100]
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = ConversationSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['conversation', 'content']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewed_user = UserSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewed_user', 'campaign', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewed_user', 'campaign', 'rating', 'comment']


class CampaignAnalyticsSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer(read_only=True)
    
    class Meta:
        model = CampaignAnalytics
        fields = ['id', 'campaign', 'total_views', 'unique_views', 'total_clicks', 
                  'conversion_rate', 'roi', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    campaign = CampaignSerializer(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'activity_type', 'campaign', 'created_at']
        read_only_fields = ['id', 'created_at']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'phone_code', 'currency', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'code', 'symbol', 'exchange_rate_to_usd', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'plan_type', 'user_type', 'price', 'currency', 
                  'duration_days', 'features', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    plan = SubscriptionPlanSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'status', 'auto_renew', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subscription = SubscriptionSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'subscription', 'transaction_type', 'status', 'amount', 
                  'currency', 'payment_method', 'payment_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'method_type', 'description', 'account_number', 
                  'phone_number', 'bank_name', 'instructions', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ManualPaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subscription_plan = SubscriptionPlanSerializer(read_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    
    class Meta:
        model = ManualPayment
        fields = ['id', 'user', 'subscription_plan', 'payment_method', 'amount', 'currency', 
                  'status', 'proof_document', 'transaction_reference', 'payment_date', 
                  'notes', 'reviewed_by', 'reviewed_at', 'rejection_reason', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ManualPaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualPayment
        fields = ['subscription_plan', 'payment_method', 'amount', 'currency', 
                  'proof_document', 'transaction_reference', 'payment_date', 'notes']


class SiteSettingsSerializer(serializers.ModelSerializer):
    default_currency = CurrencySerializer(read_only=True)
    
    class Meta:
        model = SiteSettings
        fields = ['id', 'default_currency', 'site_name', 'site_description', 'contact_email', 
                  'contact_phone', 'enable_free_plan', 'enable_pro_plan', 'enable_enterprise_plan', 
                  'enable_manual_payments', 'payment_instructions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
