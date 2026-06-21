"""
Migration qui retire SubscriptionPlan, Subscription et Transaction de l'état
de l'app `core`. Ces modèles ont été déplacés dans l'app `billing` (migration
billing/0001_initial). On utilise SeparateDatabaseAndState pour ne pas toucher
les tables existantes (core_subscriptionplan, core_subscription, core_transaction).
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0001_initial"),
        ("core", "0003_subscription_transaction_subscriptionplan_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel("Transaction"),
                migrations.DeleteModel("Subscription"),
                migrations.DeleteModel("SubscriptionPlan"),
            ],
            database_operations=[],
        ),
    ]
