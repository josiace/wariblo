from django.db import models
from advertisers.models import AdvertiserProfile


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('completed', 'Completed'),
    ]
    
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter/X'),
        ('facebook', 'Facebook'),
        ('multiple', 'Multiple Platforms'),
    ]
    
    advertiser = models.ForeignKey(AdvertiserProfile, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    niche = models.CharField(max_length=50)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_open(self):
        return self.status == 'open'
    
    @property
    def applications_count(self):
        return self.applications.count()

