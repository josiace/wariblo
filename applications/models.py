from django.db import models
from campaigns.models import Campaign
from influencers.models import InfluencerProfile


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='applications')
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='applications')
    pitch = models.TextField()
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        unique_together = ['campaign', 'influencer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.influencer.full_name} - {self.campaign.title}"
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_accepted(self):
        return self.status == 'accepted'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'

