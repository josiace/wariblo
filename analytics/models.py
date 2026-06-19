from django.db import models
from django.core.validators import MinValueValidator
from campaigns.models import Campaign
from accounts.models import User


class CampaignAnalytics(models.Model):
    """Modèle pour stocker les analytics des campagnes"""
    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.CASCADE,
        related_name='analytics',
        verbose_name="Campagne"
    )
    
    # Statistiques de vues
    total_views = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Vues totales"
    )
    unique_views = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Vues uniques"
    )
    
    # Statistiques d'engagement
    total_clicks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Clics totaux"
    )
    total_shares = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Partages totaux"
    )
    
    # Statistiques de conversion
    conversion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Taux de conversion (%)"
    )
    
    # ROI (Return on Investment)
    roi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="ROI"
    )
    
    # Engagement rate
    engagement_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Taux d'engagement (%)"
    )
    
    # Dates
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )
    
    class Meta:
        verbose_name = "Analytics de campagne"
        verbose_name_plural = "Analytics des campagnes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Analytics - {self.campaign.title}"
    
    @property
    def click_through_rate(self):
        """Calcule le taux de clic (CTR)"""
        if self.total_views > 0:
            return (self.total_clicks / self.total_views) * 100
        return 0
    
    @property
    def share_rate(self):
        """Calcule le taux de partage"""
        if self.total_views > 0:
            return (self.total_shares / self.total_views) * 100
        return 0


class UserActivity(models.Model):
    """Modèle pour suivre l'activité des utilisateurs"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name="Utilisateur"
    )
    
    ACTIVITY_TYPES = [
        ('view', 'Vue'),
        ('click', 'Clic'),
        ('apply', 'Candidature'),
        ('share', 'Partage'),
        ('message', 'Message'),
        ('review', 'Avis'),
    ]
    
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES,
        verbose_name="Type d'activité"
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='activities',
        null=True,
        blank=True,
        verbose_name="Campagne"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Métadonnées"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'activité"
    )
    
    class Meta:
        verbose_name = "Activité utilisateur"
        verbose_name_plural = "Activités des utilisateurs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['campaign', 'activity_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"
