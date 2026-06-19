from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from campaigns.models import Campaign


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    ]
    
    CATEGORY_CHOICES = [
        ('communication', 'Communication'),
        ('professionalism', 'Professionnalisme'),
        ('quality', 'Qualité du travail'),
        ('timeliness', 'Respect des délais'),
        ('overall', 'Note globale'),
    ]
    
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='overall',
        verbose_name="Catégorie"
    )
    comment = models.TextField(verbose_name="Commentaire")
    is_verified = models.BooleanField(default=False, verbose_name="Avis vérifié")
    helpful_count = models.IntegerField(default=0, verbose_name="Votes utiles")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")
    
    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        unique_together = ['reviewer', 'reviewed_user', 'campaign', 'category']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer.email} → {self.reviewed_user.email} ({self.rating}/5)"
    
    @property
    def average_rating(self):
        """Calcule la moyenne des notes pour un utilisateur"""
        reviews = self.reviewed_user.reviews_received.filter(category='overall')
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
    
    @property
    def rating_percentage(self):
        """Retourne le pourcentage de la note"""
        return (self.rating / 5) * 100
