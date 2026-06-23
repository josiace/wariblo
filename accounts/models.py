from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from core.models import Country


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('influencer', 'Influenceur'),
        ('advertiser', 'Annonceur'),
        ('admin', 'Administrateur'),
    ]

    objects = UserManager()
    username = None  # Désactiver le champ username par défaut
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='influencer', verbose_name="Rôle")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Pays")
    is_profile_complete = models.BooleanField(default=False, verbose_name="Profil complet")
    trust_score = models.IntegerField(default=50, verbose_name="Score de confiance")  # 0-100
    is_verified = models.BooleanField(default=False, verbose_name="Vérifié")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']
    
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

