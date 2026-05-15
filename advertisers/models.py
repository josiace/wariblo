from django.db import models
from accounts.models import User


class AdvertiserProfile(models.Model):
    INDUSTRY_CHOICES = [
        ('fashion', 'Fashion & Apparel'),
        ('tech', 'Technology'),
        ('food', 'Food & Beverage'),
        ('health', 'Health & Wellness'),
        ('finance', 'Finance & Banking'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('travel', 'Travel & Hospitality'),
        ('beauty', 'Beauty & Cosmetics'),
        ('fitness', 'Fitness & Sports'),
        ('automotive', 'Automotive'),
        ('retail', 'Retail & E-commerce'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='advertiser_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    website = models.URLField(null=True, blank=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='advertisers/', null=True, blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Advertiser Profile'
        verbose_name_plural = 'Advertiser Profiles'
    
    def __str__(self):
        return self.company_name

