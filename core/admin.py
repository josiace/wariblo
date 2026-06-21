from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta

from .models import Country, Currency, SubscriptionPlan, Subscription, Transaction, PaymentMethod, ManualPayment, SiteSettings


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        "get_flag",
        "name",
        "code",
        "phone_code",
        "get_currency",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "currency"]
    search_fields = ["name", "code", "phone_code"]
    list_editable = ["is_active"]
    list_per_page = 20
    ordering = ["name"]

    fieldsets = (
        (
            "Informations générales",
            {"fields": ("name", "code", "flag_emoji", "phone_code")},
        ),
        ("Devise", {"fields": ("currency",)}),
        ("Statut", {"fields": ("is_active",)}),
    )

    def get_flag(self, obj):
        return format_html('<span style="font-size: 24px;">{}</span>', obj.flag_emoji)

    get_flag.short_description = "Drapeau"

    def get_currency(self, obj):
        if obj.currency:
            return format_html(
                '<span style="color: #FF4500; font-weight: bold;">{} {}</span>',
                obj.currency.symbol,
                obj.currency.code,
            )
        return "—"

    get_currency.short_description = "Devise"


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
        "get_symbol",
        "code",
        "name",
        "exchange_rate_to_usd",
        "last_updated",
        "is_active",
    ]
    list_filter = ["is_active"]
    search_fields = ["code", "name"]
    list_editable = ["is_active", "exchange_rate_to_usd"]
    readonly_fields = ["last_updated"]
    list_per_page = 20
    ordering = ["code"]

    fieldsets = (
        ("Informations générales", {"fields": ("code", "name", "symbol")}),
        ("Taux de change", {"fields": ("exchange_rate_to_usd",)}),
        ("Statut", {"fields": ("is_active", "last_updated")}),
    )

    def get_symbol(self, obj):
        return format_html(
            '<span style="font-size: 20px; color: #FF4500; font-weight: bold;">{}</span>',
            obj.symbol,
        )

    get_symbol.short_description = "Symbole"


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'user_type', 'price', 'currency', 'is_active']
    list_filter = ['plan_type', 'user_type', 'is_active']
    search_fields = ['name']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['status', 'auto_renew', 'plan']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'status', 'amount', 'currency', 'created_at']
    list_filter = ['transaction_type', 'status', 'currency']
    search_fields = ['user__email', 'payment_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'method_type', 'is_active', 'created_at']
    list_filter = ['method_type', 'is_active']
    search_fields = ['name']


@admin.register(ManualPayment)
class ManualPaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription_plan', 'payment_method', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'subscription_plan']
    search_fields = ['user__email', 'transaction_reference']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['approve_payments', 'reject_payments']
    
    def approve_payments(self, request, queryset):
        """Approuver les paiements sélectionnés"""
        count = 0
        for payment in queryset.filter(status='pending'):
            # Créer l'abonnement
            start_date = timezone.now()
            end_date = start_date + timedelta(days=30)
            
            subscription = Subscription.objects.create(
                user=payment.user,
                plan=payment.subscription_plan,
                status='active',
                start_date=start_date,
                end_date=end_date,
                payment_method=payment.payment_method.name,
                payment_id=f"MANUAL-{payment.id}"
            )
            
            # Créer la transaction
            Transaction.objects.create(
                user=payment.user,
                transaction_type='subscription',
                status='completed',
                amount=payment.amount,
                currency=payment.currency,
                subscription=subscription,
                commission_rate=0,
                commission_amount=0,
                description=f"Abonnement {payment.subscription_plan.name} (paiement manuel)",
                payment_id=f"MANUAL-{payment.id}"
            )
            
            # Marquer le paiement comme confirmé
            payment.status = 'confirmed'
            payment.reviewed_by = request.user
            payment.reviewed_at = timezone.now()
            payment.save()
            
            count += 1
        
        self.message_user(request, f"{count} paiement(s) approuvé(s) avec succès.")
    
    approve_payments.short_description = "Approuver les paiements sélectionnés"
    
    def reject_payments(self, request, queryset):
        """Rejeter les paiements sélectionnés"""
        count = 0
        for payment in queryset.filter(status='pending'):
            payment.status = 'rejected'
            payment.reviewed_by = request.user
            payment.reviewed_at = timezone.now()
            payment.save()
            count += 1
        
        self.message_user(request, f"{count} paiement(s) rejeté(s).")
    
    reject_payments.short_description = "Rejeter les paiements sélectionnés"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Interface admin pour la configuration du site"""
    list_display = ['site_name', 'default_currency', 'contact_email', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('site_name', 'site_description', 'contact_email', 'contact_phone')
        }),
        ('Devise et Monnaie', {
            'fields': ('default_currency',)
        }),
        ('Configuration des abonnements', {
            'fields': ('enable_free_plan', 'enable_pro_plan', 'enable_enterprise_plan')
        }),
        ('Configuration des paiements', {
            'fields': ('enable_manual_payments', 'payment_instructions')
        }),
    )
    
    def has_add_permission(self, request):
        """Empêcher la création de multiples configurations"""
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Empêcher la suppression de la configuration"""
        return False
