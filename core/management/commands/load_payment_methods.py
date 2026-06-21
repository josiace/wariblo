from django.core.management.base import BaseCommand
from core.models import PaymentMethod, Currency


class Command(BaseCommand):
    help = 'Charge les méthodes de paiement par défaut pour le Mali'

    def handle(self, *args, **options):
        # Obtenir ou créer la devise FCFA
        fcfa, _ = Currency.objects.get_or_create(
            code='XOF',
            defaults={
                'name': 'Franc CFA d\'Afrique de l\'Ouest',
                'symbol': 'FCFA',
                'exchange_rate_to_usd': 0.0016,
                'is_active': True
            }
        )

        # Méthodes de paiement pour le Mali
        payment_methods = [
            {
                'name': 'Orange Money Mali',
                'method_type': 'mobile_money',
                'description': 'Paiement via Orange Money - Service de transfert d\'argent mobile',
                'phone_number': '+223 XX XX XX XX',
                'instructions': 'Envoyez le montant via Orange Money au numéro indiqué. Mentionnez votre email dans le message de transaction.',
                'is_active': True
            },
            {
                'name': 'Wave Mali',
                'method_type': 'mobile_money',
                'description': 'Paiement via Wave - Application de transfert d\'argent',
                'phone_number': '+223 XX XX XX XX',
                'instructions': 'Envoyez le montant via Wave au numéro indiqué. Mentionnez votre email dans le message de transaction.',
                'is_active': True
            },
            {
                'name': 'Malitel Money',
                'method_type': 'mobile_money',
                'description': 'Paiement via Malitel Money - Service de transfert d\'argent mobile',
                'phone_number': '+223 XX XX XX XX',
                'instructions': 'Envoyez le montant via Malitel Money au numéro indiqué. Mentionnez votre email dans le message de transaction.',
                'is_active': True
            },
            {
                'name': 'Virement bancaire BDM SA',
                'method_type': 'bank_transfer',
                'description': 'Virement bancaire via BDM SA',
                'account_number': 'XXXX XXXX XXXX XXXX',
                'bank_name': 'BDM SA',
                'instructions': 'Effectuez un virement vers le compte bancaire indiqué. Incluez votre email dans la référence du virement.',
                'is_active': True
            },
            {
                'name': 'Virement bancaire Ecobank Mali',
                'method_type': 'bank_transfer',
                'description': 'Virement bancaire via Ecobank Mali',
                'account_number': 'XXXX XXXX XXXX XXXX',
                'bank_name': 'Ecobank Mali',
                'instructions': 'Effectuez un virement vers le compte bancaire indiqué. Incluez votre email dans la référence du virement.',
                'is_active': True
            },
            {
                'name': 'Espèces',
                'method_type': 'cash',
                'description': 'Paiement en espèces au bureau',
                'instructions': 'Contactez-nous pour organiser un paiement en espèces à notre bureau.',
                'is_active': True
            },
        ]

        created_count = 0
        updated_count = 0

        for method_data in payment_methods:
            method, created = PaymentMethod.objects.get_or_create(
                name=method_data['name'],
                defaults=method_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Créé: {method.name}')
                )
            else:
                # Mettre à jour les informations existantes
                for key, value in method_data.items():
                    setattr(method, key, value)
                method.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Mis à jour: {method.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nRésumé:\n'
                f'- {created_count} méthode(s) créée(s)\n'
                f'- {updated_count} méthode(s) mise(s) à jour\n'
                f'- Total: {created_count + updated_count} méthode(s)'
            )
        )
