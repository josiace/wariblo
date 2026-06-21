from django.core.management.base import BaseCommand

from core.models import SubscriptionPlan, Currency


class Command(BaseCommand):
    help = "Charge les plans d'abonnement par défaut"

    def handle(self, *args, **options):
        self.stdout.write("Chargement des plans d'abonnement par défaut...")

        # Obtenir ou créer la devise USD
        usd, created = Currency.objects.get_or_create(
            code="USD",
            defaults={
                "name": "US Dollar",
                "symbol": "$",
                "exchange_rate_to_usd": 1.0,
                "is_active": True,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Devise USD créée"))

        # Plans pour les influenceurs
        influencer_plans = [
            {
                "name": "Gratuit",
                "plan_type": "free",
                "user_type": "influencer",
                "price": 0,
                "currency": usd,
                "max_campaigns": 5,
                "max_applications": 10,
                "max_messages": 20,
                "can_access_analytics": False,
                "can_access_advanced_search": False,
                "can_create_unlimited_campaigns": False,
                "priority_support": False,
                "verified_badge": False,
                "commission_rate": 20.00,
            },
            {
                "name": "Pro",
                "plan_type": "pro",
                "user_type": "influencer",
                "price": 9.00,
                "currency": usd,
                "max_campaigns": 20,
                "max_applications": 50,
                "max_messages": 100,
                "can_access_analytics": True,
                "can_access_advanced_search": True,
                "can_create_unlimited_campaigns": False,
                "priority_support": False,
                "verified_badge": True,
                "commission_rate": 15.00,
            },
            {
                "name": "Enterprise",
                "plan_type": "enterprise",
                "user_type": "influencer",
                "price": 29.00,
                "currency": usd,
                "max_campaigns": 999,
                "max_applications": 999,
                "max_messages": 999,
                "can_access_analytics": True,
                "can_access_advanced_search": True,
                "can_create_unlimited_campaigns": True,
                "priority_support": True,
                "verified_badge": True,
                "commission_rate": 10.00,
            },
        ]

        # Plans pour les annonceurs
        advertiser_plans = [
            {
                "name": "Gratuit",
                "plan_type": "free",
                "user_type": "advertiser",
                "price": 0,
                "currency": usd,
                "max_campaigns": 3,
                "max_applications": 999,
                "max_messages": 30,
                "can_access_analytics": False,
                "can_access_advanced_search": False,
                "can_create_unlimited_campaigns": False,
                "priority_support": False,
                "verified_badge": False,
                "commission_rate": 20.00,
            },
            {
                "name": "Pro",
                "plan_type": "pro",
                "user_type": "advertiser",
                "price": 29.00,
                "currency": usd,
                "max_campaigns": 15,
                "max_applications": 999,
                "max_messages": 150,
                "can_access_analytics": True,
                "can_access_advanced_search": True,
                "can_create_unlimited_campaigns": False,
                "priority_support": False,
                "verified_badge": True,
                "commission_rate": 15.00,
            },
            {
                "name": "Enterprise",
                "plan_type": "enterprise",
                "user_type": "advertiser",
                "price": 99.00,
                "currency": usd,
                "max_campaigns": 999,
                "max_applications": 999,
                "max_messages": 999,
                "can_access_analytics": True,
                "can_access_advanced_search": True,
                "can_create_unlimited_campaigns": True,
                "priority_support": True,
                "verified_badge": True,
                "commission_rate": 10.00,
            },
        ]

        # Créer ou mettre à jour les plans
        all_plans = influencer_plans + advertiser_plans
        created_count = 0
        updated_count = 0

        for plan_data in all_plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data["name"],
                user_type=plan_data["user_type"],
                defaults=plan_data,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Plan créé: {plan.name} ({plan.user_type})")
                )
            else:
                # Mettre à jour le plan existant
                for key, value in plan_data.items():
                    setattr(plan, key, value)
                plan.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Plan mis à jour: {plan.name} ({plan.user_type})"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nChargement terminé: {created_count} plans créés, {updated_count} plans mis à jour"
            )
        )
