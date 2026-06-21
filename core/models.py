from django.conf import settings
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du pays")
    code = models.CharField(max_length=3, unique=True, verbose_name="Code ISO")
    phone_code = models.CharField(max_length=5, verbose_name="Indicatif téléphonique")
    flag_emoji = models.CharField(
        max_length=10, blank=True, verbose_name="Drapeau emoji"
    )
    currency = models.ForeignKey(
        "Currency",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Devise par défaut",
        related_name="countries",
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"
        ordering = ["name"]

    def __str__(self):
        return f"{self.flag_emoji} {self.name} (+{self.phone_code})"


class Currency(models.Model):
    code = models.CharField(
        max_length=3, unique=True, verbose_name="Code ISO (ex: USD, EUR)"
    )
    name = models.CharField(max_length=50, verbose_name="Nom de la monnaie")
    symbol = models.CharField(max_length=5, verbose_name="Symbole (ex: $, €)")
    exchange_rate_to_usd = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        default=1.0,
        verbose_name="Taux de change vers USD",
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Dernière mise à jour"
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Devise"
        verbose_name_plural = "Devises"
        ordering = ["code"]

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


class SubscriptionPlan(models.Model):
    PLAN_TYPES = [
        ("free", "Gratuit"),
        ("pro", "Pro"),
        ("enterprise", "Enterprise"),
    ]

    USER_TYPES = [
        ("influencer", "Influenceur"),
        ("advertiser", "Annonceur"),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom du plan")
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, verbose_name="Type de plan")
    user_type = models.CharField(max_length=20, choices=USER_TYPES, verbose_name="Type d'utilisateur")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix mensuel")
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, verbose_name="Devise")

    # Limites
    max_campaigns = models.IntegerField(default=3, verbose_name="Max campagnes/mois")
    max_applications = models.IntegerField(default=10, verbose_name="Max candidatures/mois")
    max_messages = models.IntegerField(default=50, verbose_name="Max messages/mois")

    # Fonctionnalités
    can_access_analytics = models.BooleanField(default=False, verbose_name="Accès analytics")
    can_access_advanced_search = models.BooleanField(default=False, verbose_name="Recherche avancée")
    can_create_unlimited_campaigns = models.BooleanField(default=False, verbose_name="Campagnes illimitées")
    priority_support = models.BooleanField(default=False, verbose_name="Support prioritaire")
    verified_badge = models.BooleanField(default=False, verbose_name="Badge vérifié")

    # Commission
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=15.00,
        verbose_name="Taux de commission (%)",
    )

    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plan d'abonnement"
        verbose_name_plural = "Plans d'abonnement"
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()}) - {self.price} {self.currency.symbol if self.currency else 'USD'}/mois"


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("active", "Actif"),
        ("cancelled", "Annulé"),
        ("expired", "Expiré"),
        ("pending", "En attente"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Statut"
    )

    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    auto_renew = models.BooleanField(
        default=True, verbose_name="Renouvellement automatique"
    )

    # Paiement
    payment_method = models.CharField(
        max_length=50, blank=True, verbose_name="Méthode de paiement"
    )
    payment_id = models.CharField(
        max_length=100, blank=True, verbose_name="ID de paiement"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    def is_active_subscription(self):
        from django.utils import timezone
        return self.status == "active" and self.end_date > timezone.now()

    def days_remaining(self):
        from django.utils import timezone
        if self.end_date:
            return (self.end_date - timezone.now()).days
        return 0


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("commission", "Commission"),
        ("subscription", "Abonnement"),
        ("refund", "Remboursement"),
        ("bonus", "Bonus"),
    ]

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("completed", "Complété"),
        ("failed", "Échoué"),
        ("refunded", "Remboursé"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES, verbose_name="Type de transaction"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Statut"
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Montant"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Devise",
    )

    # Référence
    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    application = models.ForeignKey(
        "applications.Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    # Commission
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Taux de commission (%)"
    )
    commission_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Montant de la commission"
    )

    description = models.TextField(blank=True, verbose_name="Description")
    payment_id = models.CharField(
        max_length=100, blank=True, verbose_name="ID de paiement"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency.symbol if self.currency else 'USD'}"


class PaymentMethod(models.Model):
    """Méthodes de paiement disponibles"""
    METHOD_TYPES = [
        ('bank_transfer', 'Virement bancaire'),
        ('mobile_money', 'Mobile Money (Orange Money, Wave, etc.)'),
        ('cash', 'Espèces'),
        ('check', 'Chèque'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom")
    method_type = models.CharField(max_length=20, choices=METHOD_TYPES, verbose_name="Type")
    description = models.TextField(blank=True, verbose_name="Description")
    account_number = models.CharField(max_length=50, blank=True, verbose_name="Numéro de compte")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Nom de la banque")
    instructions = models.TextField(blank=True, verbose_name="Instructions de paiement")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Méthode de paiement"
        verbose_name_plural = "Méthodes de paiement"
    
    def __str__(self):
        return self.name


class ManualPayment(models.Model):
    """Paiements manuels pour les abonnements"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('rejected', 'Rejeté'),
        ('cancelled', 'Annulé'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='manual_payments'
    )
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name='manual_payments'
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name='manual_payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Devise"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Statut"
    )
    
    # Preuve de paiement
    proof_document = models.FileField(
        upload_to='payment_proofs/',
        blank=True,
        null=True,
        verbose_name="Preuve de paiement"
    )
    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Référence de transaction"
    )
    payment_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de paiement"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Administration
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_payments'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, verbose_name="Raison du rejet")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Paiement manuel"
        verbose_name_plural = "Paiements manuels"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Paiement de {self.user.email} - {self.subscription_plan.name}"


class SiteSettings(models.Model):
    """Configuration globale du site"""
    default_currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Devise par défaut"
    )
    site_name = models.CharField(max_length=100, default="Wariblo", verbose_name="Nom du site")
    site_description = models.TextField(blank=True, verbose_name="Description du site")
    contact_email = models.EmailField(blank=True, verbose_name="Email de contact")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone de contact")
    
    # Configuration des abonnements
    enable_free_plan = models.BooleanField(default=True, verbose_name="Activer le plan gratuit")
    enable_pro_plan = models.BooleanField(default=True, verbose_name="Activer le plan Pro")
    enable_enterprise_plan = models.BooleanField(default=True, verbose_name="Activer le plan Enterprise")
    
    # Configuration des paiements
    enable_manual_payments = models.BooleanField(default=True, verbose_name="Activer les paiements manuels")
    payment_instructions = models.TextField(blank=True, verbose_name="Instructions de paiement")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configurations du site"
    
    def __str__(self):
        return f"Configuration - {self.site_name}"
    
    @classmethod
    def get_settings(cls):
        """Récupérer ou créer les paramètres du site"""
        settings_obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Wariblo',
                'site_description': 'Plateforme de Marketing d\'Influence en Afrique',
                'contact_email': 'contact@wariblo.com',
            }
        )
        return settings_obj


# Les modèles de monétisation sont définis ici directement
# Plus besoin d'import depuis billing.models

__all__ = [
    "Country",
    "Currency",
    "SubscriptionPlan",
    "Subscription",
    "Transaction",
    "PaymentMethod",
    "ManualPayment",
    "SiteSettings",
]
