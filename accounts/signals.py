from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile automatically when user is created"""
    if created:
        if instance.role == 'influencer':
            from influencers.models import InfluencerProfile
            InfluencerProfile.objects.create(user=instance)
        elif instance.role == 'advertiser':
            from advertisers.models import AdvertiserProfile
            AdvertiserProfile.objects.create(user=instance)
