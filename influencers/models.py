from django.db import models
from accounts.models import User


class InfluencerProfile(models.Model):
    NICHE_CHOICES = [
        ('fashion', 'Fashion'),
        ('tech', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('fitness', 'Fitness & Health'),
        ('food', 'Food & Cooking'),
        ('travel', 'Travel'),
        ('beauty', 'Beauty'),
        ('gaming', 'Gaming'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    full_name = models.CharField(max_length=200)
    bio = models.TextField()
    niche = models.CharField(max_length=50, choices=NICHE_CHOICES)
    instagram_followers = models.PositiveIntegerField(default=0)
    tiktok_followers = models.PositiveIntegerField(default=0)
    youtube_subscribers = models.PositiveIntegerField(default=0)
    twitter_followers = models.PositiveIntegerField(default=0)
    rate_per_post = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profile_image = models.ImageField(upload_to='influencers/', null=True, blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Influencer Profile'
        verbose_name_plural = 'Influencer Profiles'
    
    def __str__(self):
        return self.full_name
    
    @property
    def total_followers(self):
        return self.instagram_followers + self.tiktok_followers + self.youtube_subscribers + self.twitter_followers

