from django import forms
from django.core.exceptions import ValidationError
from .models import InfluencerProfile


class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = ['full_name', 'bio', 'niche', 'instagram_followers', 'tiktok_followers', 
                  'youtube_subscribers', 'twitter_followers', 'rate_per_post', 'profile_image', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'instagram_followers': forms.NumberInput(attrs={'min': 0}),
            'tiktok_followers': forms.NumberInput(attrs={'min': 0}),
            'youtube_subscribers': forms.NumberInput(attrs={'min': 0}),
            'twitter_followers': forms.NumberInput(attrs={'min': 0}),
            'rate_per_post': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_rate_per_post(self):
        rate = self.cleaned_data.get('rate_per_post')
        if rate is not None and rate < 0:
            raise ValidationError("Rate per post cannot be negative.")
        return rate
    
    def clean(self):
        cleaned_data = super().clean()
        instagram = cleaned_data.get('instagram_followers', 0)
        tiktok = cleaned_data.get('tiktok_followers', 0)
        youtube = cleaned_data.get('youtube_subscribers', 0)
        twitter = cleaned_data.get('twitter_followers', 0)
        
        total = instagram + tiktok + youtube + twitter
        if total == 0:
            raise ValidationError("Please provide at least one social media follower count.")
        
        return cleaned_data
