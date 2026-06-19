from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from campaigns.models import Campaign
from applications.models import Application
from influencers.models import InfluencerProfile
from .serializers import (
    CampaignSerializer, 
    ApplicationSerializer, 
    ApplicationCreateSerializer,
    InfluencerProfileSerializer
)


class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les campagnes
    """
    queryset = Campaign.objects.filter(status='open').select_related(
        'advertiser__user'
    ).prefetch_related('applications__influencer__user')
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['niche', 'platform', 'status', 'deadline']
    search_fields = ['title', 'description', 'requirements']
    ordering_fields = ['created_at', 'budget', 'deadline']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Récupérer les applications pour une campagne spécifique
        """
        campaign = self.get_object()
        applications = campaign.applications.select_related('influencer__user')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


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


class InfluencerProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les profils influenceurs
    """
    queryset = InfluencerProfile.objects.select_related('user')
    serializer_class = InfluencerProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['niche', 'location']
    search_fields = ['full_name', 'bio']
    ordering_fields = ['created_at', 'total_followers']
    ordering = ['-total_followers']
    
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
