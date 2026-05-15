from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Country


class User(AbstractUser):
    ROLE_CHOICES = [
        ('influencer', 'Influenceur'),
        ('advertiser', 'Annonceur'),
        ('admin', 'Administrateur'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='influencer', verbose_name="Rôle")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Pays")
    is_profile_complete = models.BooleanField(default=False, verbose_name="Profil complet")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return self.email
    
    @property
    def is_influencer(self):
        return self.role == 'influencer'
    
    @property
    def is_advertiser(self):
        return self.role == 'advertiser'
    
    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser

