from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du pays")
    code = models.CharField(max_length=3, unique=True, verbose_name="Code ISO")
    phone_code = models.CharField(max_length=5, verbose_name="Indicatif téléphonique")
    flag_emoji = models.CharField(max_length=10, blank=True, verbose_name="Drapeau emoji")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.flag_emoji} {self.name} (+{self.phone_code})"

