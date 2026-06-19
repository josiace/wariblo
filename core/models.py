from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du pays")
    code = models.CharField(max_length=3, unique=True, verbose_name="Code ISO")
    phone_code = models.CharField(max_length=5, verbose_name="Indicatif téléphonique")
    flag_emoji = models.CharField(max_length=10, blank=True, verbose_name="Drapeau emoji")
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Devise par défaut",
        related_name='countries'
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.flag_emoji} {self.name} (+{self.phone_code})"


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name="Code ISO (ex: USD, EUR)")
    name = models.CharField(max_length=50, verbose_name="Nom de la monnaie")
    symbol = models.CharField(max_length=5, verbose_name="Symbole (ex: $, €)")
    exchange_rate_to_usd = models.DecimalField(
        max_digits=10, 
        decimal_places=6, 
        default=1.0,
        verbose_name="Taux de change vers USD"
    )
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Devise"
        verbose_name_plural = "Devises"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.symbol} {self.code}"
    
    def convert_from_usd(self, amount_usd):
        """Convertir un montant USD vers cette devise"""
        if self.exchange_rate_to_usd == 0:
            return amount_usd
        from decimal import Decimal
        amount = Decimal(str(amount_usd))
        rate = Decimal(str(self.exchange_rate_to_usd))
        return float(amount / rate)
    
    def convert_to_usd(self, amount):
        """Convertir un montant de cette devise vers USD"""
        from decimal import Decimal
        amount = Decimal(str(amount))
        rate = Decimal(str(self.exchange_rate_to_usd))
        return float(amount * rate)

