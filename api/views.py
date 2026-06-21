from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from campaigns.models import Campaign
from applications.models import Application
from influencers.models import InfluencerProfile
from advertisers.models import AdvertiserProfile
from accounts.models import User
from messaging.models import Conversation, Message
from reviews.models import Review
from analytics.models import CampaignAnalytics, UserActivity
from core.models import Country, Currency, SubscriptionPlan, Subscription, Transaction, PaymentMethod, ManualPayment, SiteSettings
from .serializers import (
    CampaignSerializer, 
    ApplicationSerializer, 
    ApplicationCreateSerializer,
    InfluencerProfileSerializer,
    InfluencerProfileCreateSerializer,
    AdvertiserProfileSerializer,
    AdvertiserProfileCreateSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
    ConversationSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
    CampaignAnalyticsSerializer,
    UserActivitySerializer,
    CountrySerializer,
    CurrencySerializer,
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    TransactionSerializer,
    PaymentMethodSerializer,
    ManualPaymentSerializer,
    ManualPaymentCreateSerializer,
    SiteSettingsSerializer,
)


@api_view(['POST'])
def register(request):
    """
    API endpoint pour l'inscription
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    API endpoint pour la connexion
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    """
    API endpoint pour la déconnexion
    """
    if request.user.is_authenticated:
        try:
            request.user.auth_token.delete()
        except:
            pass
    return Response({'message': 'Déconnexion réussie'})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'country']
    search_fields = ['email', 'username', 'full_name']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Récupérer le profil de l'utilisateur connecté
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class InfluencerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les profils influenceurs
    """
    queryset = InfluencerProfile.objects.select_related('user')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['niche', 'location']
    search_fields = ['full_name', 'bio']
    ordering_fields = ['created_at', 'instagram_followers']
    ordering = ['-instagram_followers']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InfluencerProfileCreateSerializer
        return InfluencerProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """
        Récupérer le profil de l'influenceur connecté
        """
        try:
            influencer = request.user.influencer_profile
            serializer = self.get_serializer(influencer)
            return Response(serializer.data)
        except InfluencerProfile.DoesNotExist:
            return Response(
                {'error': 'Profil influenceur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class AdvertiserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les profils annonceurs
    """
    queryset = AdvertiserProfile.objects.select_related('user')
    serializer_class = AdvertiserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['industry', 'location']
    search_fields = ['company_name', 'company_description']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AdvertiserProfileCreateSerializer
        return AdvertiserProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """
        Récupérer le profil de l'annonceur connecté
        """
        try:
            advertiser = request.user.advertiser_profile
            serializer = self.get_serializer(advertiser)
            return Response(serializer.data)
        except AdvertiserProfile.DoesNotExist:
            return Response(
                {'error': 'Profil annonceur non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class CampaignViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les campagnes
    """
    queryset = Campaign.objects.select_related('advertiser__user').prefetch_related('applications__influencer__user')
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['niche', 'platform', 'status', 'deadline']
    search_fields = ['title', 'description', 'requirements']
    ordering_fields = ['created_at', 'budget', 'deadline']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CampaignCreateSerializer
        return CampaignSerializer
    
    def perform_create(self, serializer):
        try:
            advertiser = self.request.user.advertiser_profile
            serializer.save(advertiser=advertiser)
        except AdvertiserProfile.DoesNotExist:
            return Response(
                {'error': 'Profil annonceur non trouvé'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Récupérer les applications pour une campagne spécifique
        """
        campaign = self.get_object()
        applications = campaign.applications.select_related('influencer__user')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_campaigns(self, request):
        """
        Récupérer les campagnes de l'annonceur connecté
        """
        try:
            advertiser = request.user.advertiser_profile
            campaigns = self.queryset.filter(advertiser=advertiser)
            serializer = self.get_serializer(campaigns, many=True)
            return Response(serializer.data)
        except AdvertiserProfile.DoesNotExist:
            return Response(
                {'error': 'Profil annonceur non trouvé'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les applications
    """
    queryset = Application.objects.select_related(
        'campaign__advertiser__user',
        'influencer__user'
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'campaign', 'influencer']
    search_fields = ['pitch']
    ordering_fields = ['created_at', 'proposed_price']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationSerializer
    
    def perform_create(self, serializer):
        """
        Créer une application avec l'influenceur connecté
        """
        try:
            influencer = self.request.user.influencer_profile
            serializer.save(influencer=influencer)
        except InfluencerProfile.DoesNotExist:
            return Response(
                {'error': 'Profil influenceur non trouvé'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """
        Récupérer les applications de l'influenceur connecté
        """
        try:
            influencer = request.user.influencer_profile
            applications = self.queryset.filter(influencer=influencer)
            serializer = ApplicationSerializer(applications, many=True)
            return Response(serializer.data)
        except InfluencerProfile.DoesNotExist:
            return Response(
                {'error': 'Profil influenceur non trouvé'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les conversations
    """
    queryset = Conversation.objects.prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']
    
    @action(detail=False, methods=['get'])
    def my_conversations(self, request):
        """
        Récupérer les conversations de l'utilisateur connecté
        """
        conversations = self.queryset.filter(participants=request.user)
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Récupérer les messages d'une conversation
        """
        conversation = self.get_object()
        messages = conversation.messages.all().select_related('sender')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les messages
    """
    queryset = Message.objects.select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation', 'is_read']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les avis
    """
    queryset = Review.objects.select_related('reviewer', 'reviewed_user', 'campaign')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating', 'campaign']
    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """
        Récupérer les avis de l'utilisateur connecté
        """
        reviews = self.queryset.filter(reviewer=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def reviews_about_me(self, request):
        """
        Récupérer les avis sur l'utilisateur connecté
        """
        reviews = self.queryset.filter(reviewed_user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class CampaignAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les analytics de campagnes
    """
    queryset = CampaignAnalytics.objects.select_related('campaign')
    serializer_class = CampaignAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['campaign']


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les activités utilisateurs
    """
    queryset = UserActivity.objects.select_related('user', 'campaign')
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'activity_type', 'campaign']
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """
        Récupérer les activités de l'utilisateur connecté
        """
        activities = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les pays
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code']


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les devises
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'symbol']


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les plans d'abonnement
    """
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plan_type', 'user_type', 'is_active']


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les abonnements
    """
    queryset = Subscription.objects.select_related('user', 'plan')
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'plan', 'status']
    
    @action(detail=False, methods=['get'])
    def my_subscription(self, request):
        """
        Récupérer l'abonnement de l'utilisateur connecté
        """
        try:
            subscription = self.queryset.filter(user=request.user).latest('created_at')
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response(
                {'error': 'Aucun abonnement trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les transactions
    """
    queryset = Transaction.objects.select_related('user', 'subscription', 'currency')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'subscription', 'transaction_type', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def my_transactions(self, request):
        """
        Récupérer les transactions de l'utilisateur connecté
        """
        transactions = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les méthodes de paiement
    """
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['method_type', 'is_active']


class ManualPaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les paiements manuels
    """
    queryset = ManualPayment.objects.select_related('user', 'subscription_plan', 'payment_method', 'currency')
    serializer_class = ManualPaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'subscription_plan', 'payment_method', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ManualPaymentCreateSerializer
        return ManualPaymentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        """
        Récupérer les paiements manuels de l'utilisateur connecté
        """
        payments = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)


class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les paramètres du site
    """
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Récupérer les paramètres actuels du site
        """
        settings = SiteSettings.get_settings()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)
