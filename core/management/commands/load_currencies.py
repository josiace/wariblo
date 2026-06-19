from django.core.management.base import BaseCommand
from core.models import Currency, Country


class Command(BaseCommand):
    help = 'Charge les devises principales et les associe aux pays africains'

    def handle(self, *args, **options):
        # Créer les devises principales avec leurs taux de change approximatifs
        currencies_data = [
            {'code': 'USD', 'name': 'Dollar américain', 'symbol': '$', 'rate': 1.0},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'rate': 0.92},
            {'code': 'GBP', 'name': 'Livre sterling', 'symbol': '£', 'rate': 0.79},
            {'code': 'XOF', 'name': 'Franc CFA d\'Afrique de l\'Ouest', 'symbol': 'CFA', 'rate': 600.0},
            {'code': 'XAF', 'name': 'Franc CFA d\'Afrique Centrale', 'symbol': 'CFA', 'rate': 600.0},
            {'code': 'ZAR', 'name': 'Rand sud-africain', 'symbol': 'R', 'rate': 18.5},
            {'code': 'NGN', 'name': 'Naira nigérian', 'symbol': '₦', 'rate': 1550.0},
            {'code': 'EGP', 'name': 'Livre égyptienne', 'symbol': 'E£', 'rate': 30.9},
            {'code': 'KES', 'name': 'Shilling kenyan', 'symbol': 'KSh', 'rate': 153.0},
            {'code': 'GHS', 'name': 'Cedi ghanéen', 'symbol': '₵', 'rate': 12.5},
            {'code': 'MAD', 'name': 'Dirham marocain', 'symbol': 'DH', 'rate': 9.8},
            {'code': 'TZS', 'name': 'Shilling tanzanien', 'symbol': 'TSh', 'rate': 2500.0},
            {'code': 'UGX', 'name': 'Shilling ougandais', 'symbol': 'USh', 'rate': 3800.0},
            {'code': 'ETB', 'name': 'Birr éthiopien', 'symbol': 'Br', 'rate': 56.0},
            {'code': 'CDF', 'name': 'Franc congolais', 'symbol': 'FC', 'rate': 2750.0},
            {'code': 'AOA', 'name': 'Kwanza angolais', 'symbol': 'Kz', 'rate': 850.0},
            {'code': 'BWP', 'name': 'Pula botswanais', 'symbol': 'P', 'rate': 13.5},
            {'code': 'ZMW', 'name': 'Kwacha zambien', 'symbol': 'ZK', 'rate': 25.0},
            {'code': 'MWK', 'name': 'Kwacha malawite', 'symbol': 'MK', 'rate': 1750.0},
            {'code': 'MZN', 'name': 'Metical mozambicain', 'symbol': 'MT', 'rate': 63.0},
            {'code': 'NAD', 'name': 'Dollar namibien', 'symbol': 'N$', 'rate': 18.5},
            {'code': 'SZL', 'name': 'Lilangeni swazi', 'symbol': 'L', 'rate': 18.5},
            {'code': 'LSL', 'name': 'Loti lesothan', 'symbol': 'L', 'rate': 18.5},
            {'code': 'LRD', 'name': 'Dollar libérien', 'symbol': '$', 'rate': 185.0},
            {'code': 'SLL', 'name': 'Leone sierra-léonais', 'symbol': 'Le', 'rate': 2250.0},
            {'code': 'GMD', 'name': 'Dalasi gambien', 'symbol': 'D', 'rate': 63.0},
            {'code': 'GNF', 'name': 'Franc guinéen', 'symbol': 'FG', 'rate': 870.0},
            {'code': 'BIF', 'name': 'Franc burundais', 'symbol': 'FBu', 'rate': 2850.0},
            {'code': 'RWF', 'name': 'Franc rwandais', 'symbol': 'RF', 'rate': 1250.0},
            {'code': 'DJF', 'name': 'Franc djiboutien', 'symbol': 'Fdj', 'rate': 177.0},
            {'code': 'SOS', 'name': 'Shilling somalien', 'symbol': 'Sh', 'rate': 570.0},
            {'code': 'ERN', 'name': 'Nafka érythréen', 'symbol': 'Nfk', 'rate': 15.0},
            {'code': 'SSP', 'name': 'Livre soud-soudanaise', 'symbol': '£', 'rate': 130.0},
            {'code': 'SCR', 'name': 'Roupie seychelloise', 'symbol': '₨', 'rate': 13.5},
            {'code': 'MUR', 'name': 'Roupie mauricienne', 'symbol': '₨', 'rate': 45.0},
            {'code': 'CVE', 'name': 'Escudo cap-verdien', 'symbol': '$', 'rate': 102.0},
            {'code': 'STN', 'name': 'Dobra santoméen', 'symbol': 'Db', 'rate': 2250.0},
            {'code': 'GQE', 'name': 'Franc CFA d\'Afrique Centrale', 'symbol': 'CFA', 'rate': 600.0},
        ]

        # Créer ou mettre à jour les devises
        for currency_data in currencies_data:
            currency, created = Currency.objects.update_or_create(
                code=currency_data['code'],
                defaults={
                    'name': currency_data['name'],
                    'symbol': currency_data['symbol'],
                    'exchange_rate_to_usd': currency_data['rate'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Créé: {currency}'))
            else:
                self.stdout.write(self.style.WARNING(f'Mis à jour: {currency}'))

        # Associer les devises aux pays africains
        country_currency_map = {
            'BEN': 'XOF', 'BFA': 'XOF', 'MLI': 'XOF', 'NER': 'XOF', 'SEN': 'XOF', 'TGO': 'XOF', 'CIV': 'XOF', 'GIN': 'XOF',
            'CMR': 'XAF', 'CAF': 'XAF', 'TCD': 'XAF', 'COG': 'XAF', 'GAB': 'XAF', 'GNQ': 'XAF',
            'ZAF': 'ZAR', 'LSO': 'ZAR', 'NAM': 'ZAR', 'SWZ': 'ZAR',
            'NGA': 'NGN', 'EGY': 'EGP', 'KEN': 'KES', 'GHA': 'GHS', 'MAR': 'MAD', 'TZA': 'TZS',
            'UGA': 'UGX', 'ETH': 'ETB', 'COD': 'CDF', 'AGO': 'AOA', 'BWA': 'BWP', 'ZMB': 'ZMW',
            'MWI': 'MWK', 'MOZ': 'MZN', 'NAM': 'ZAR', 'SWZ': 'ZAR', 'LSO': 'ZAR',
            'LBR': 'LRD', 'SLE': 'SLL', 'GMB': 'GMD', 'GIN': 'XOF', 'BDI': 'BIF', 'RWA': 'RWF',
            'DJI': 'DJF', 'SOM': 'SOS', 'ERI': 'ERN', 'SSD': 'SSP', 'SYC': 'SCR', 'MUS': 'MUR',
            'CPV': 'CVE', 'STP': 'STN', 'GNQ': 'XAF',
        }

        for country_code, currency_code in country_currency_map.items():
            try:
                country = Country.objects.get(code=country_code)
                currency = Currency.objects.get(code=currency_code)
                country.currency = currency
                country.save()
                self.stdout.write(self.style.SUCCESS(f'Associé: {country.name} -> {currency.code}'))
            except Country.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Pays non trouvé: {country_code}'))
            except Currency.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Devise non trouvée: {currency_code}'))

        self.stdout.write(self.style.SUCCESS('Chargement des devises terminé!'))
