from django.core.management.base import BaseCommand
from core.models import Country


class Command(BaseCommand):
    help = 'Charge les pays africains par défaut'

    def handle(self, *args, **options):
        countries_data = [
            {"name": "Afrique du Sud", "code": "ZAF", "phone_code": "27", "flag_emoji": "🇿🇦"},
            {"name": "Algérie", "code": "DZA", "phone_code": "213", "flag_emoji": "🇩🇿"},
            {"name": "Angola", "code": "AGO", "phone_code": "244", "flag_emoji": "🇦🇴"},
            {"name": "Bénin", "code": "BEN", "phone_code": "229", "flag_emoji": "🇧🇯"},
            {"name": "Botswana", "code": "BWA", "phone_code": "267", "flag_emoji": "🇧🇼"},
            {"name": "Burkina Faso", "code": "BFA", "phone_code": "226", "flag_emoji": "🇧🇫"},
            {"name": "Burundi", "code": "BDI", "phone_code": "257", "flag_emoji": "🇧🇮"},
            {"name": "Cameroun", "code": "CMR", "phone_code": "237", "flag_emoji": "🇨🇲"},
            {"name": "Cap-Vert", "code": "CPV", "phone_code": "238", "flag_emoji": "🇨🇻"},
            {"name": "Centrafrique", "code": "CAF", "phone_code": "236", "flag_emoji": "🇨🇫"},
            {"name": "Comores", "code": "COM", "phone_code": "269", "flag_emoji": "🇰🇲"},
            {"name": "Congo", "code": "COG", "phone_code": "242", "flag_emoji": "🇨🇬"},
            {"name": "Côte d'Ivoire", "code": "CIV", "phone_code": "225", "flag_emoji": "🇨🇮"},
            {"name": "Djibouti", "code": "DJI", "phone_code": "253", "flag_emoji": "🇩🇯"},
            {"name": "Égypte", "code": "EGY", "phone_code": "20", "flag_emoji": "🇪🇬"},
            {"name": "Érythrée", "code": "ERI", "phone_code": "291", "flag_emoji": "🇪🇷"},
            {"name": "Éthiopie", "code": "ETH", "phone_code": "251", "flag_emoji": "🇪🇹"},
            {"name": "Gabon", "code": "GAB", "phone_code": "241", "flag_emoji": "🇬🇦"},
            {"name": "Gambie", "code": "GMB", "phone_code": "220", "flag_emoji": "🇬🇲"},
            {"name": "Ghana", "code": "GHA", "phone_code": "233", "flag_emoji": "🇬🇭"},
            {"name": "Guinée", "code": "GIN", "phone_code": "224", "flag_emoji": "🇬🇳"},
            {"name": "Guinée-Bissau", "code": "GNB", "phone_code": "245", "flag_emoji": "🇬🇼"},
            {"name": "Guinée équatoriale", "code": "GNQ", "phone_code": "240", "flag_emoji": "🇬🇶"},
            {"name": "Kenya", "code": "KEN", "phone_code": "254", "flag_emoji": "🇰🇪"},
            {"name": "Lesotho", "code": "LSO", "phone_code": "266", "flag_emoji": "🇱🇸"},
            {"name": "Libéria", "code": "LBR", "phone_code": "231", "flag_emoji": "🇱🇷"},
            {"name": "Libye", "code": "LBY", "phone_code": "218", "flag_emoji": "🇱🇾"},
            {"name": "Madagascar", "code": "MDG", "phone_code": "261", "flag_emoji": "🇲🇬"},
            {"name": "Malawi", "code": "MWI", "phone_code": "265", "flag_emoji": "🇲🇼"},
            {"name": "Mali", "code": "MLI", "phone_code": "223", "flag_emoji": "🇲🇱"},
            {"name": "Maroc", "code": "MAR", "phone_code": "212", "flag_emoji": "🇲🇦"},
            {"name": "Mauritanie", "code": "MRT", "phone_code": "222", "flag_emoji": "🇲🇷"},
            {"name": "Maurice", "code": "MUS", "phone_code": "230", "flag_emoji": "🇲🇺"},
            {"name": "Mozambique", "code": "MOZ", "phone_code": "258", "flag_emoji": "🇲🇿"},
            {"name": "Namibie", "code": "NAM", "phone_code": "264", "flag_emoji": "🇳🇦"},
            {"name": "Niger", "code": "NER", "phone_code": "227", "flag_emoji": "🇳🇪"},
            {"name": "Nigeria", "code": "NGA", "phone_code": "234", "flag_emoji": "🇳🇬"},
            {"name": "Ouganda", "code": "UGA", "phone_code": "256", "flag_emoji": "🇺🇬"},
            {"name": "Rwanda", "code": "RWA", "phone_code": "250", "flag_emoji": "🇷🇼"},
            {"name": "Sahara occidental", "code": "ESH", "phone_code": "212", "flag_emoji": "🇪🇭"},
            {"name": "Sao Tomé-et-Principe", "code": "STP", "phone_code": "239", "flag_emoji": "🇸🇹"},
            {"name": "Sénégal", "code": "SEN", "phone_code": "221", "flag_emoji": "🇸🇳"},
            {"name": "Seychelles", "code": "SYC", "phone_code": "248", "flag_emoji": "🇸🇨"},
            {"name": "Sierra Leone", "code": "SLE", "phone_code": "232", "flag_emoji": "🇸🇱"},
            {"name": "Somalie", "code": "SOM", "phone_code": "252", "flag_emoji": "🇸🇴"},
            {"name": "Soudan", "code": "SDN", "phone_code": "249", "flag_emoji": "🇸🇩"},
            {"name": "Soudan du Sud", "code": "SSD", "phone_code": "211", "flag_emoji": "🇸🇸"},
            {"name": "Swaziland", "code": "SWZ", "phone_code": "268", "flag_emoji": "🇸🇿"},
            {"name": "Tanzanie", "code": "TZA", "phone_code": "255", "flag_emoji": "🇹🇿"},
            {"name": "Tchad", "code": "TCD", "phone_code": "235", "flag_emoji": "🇹🇩"},
            {"name": "Togo", "code": "TGO", "phone_code": "228", "flag_emoji": "🇹🇬"},
            {"name": "Tunisie", "code": "TUN", "phone_code": "216", "flag_emoji": "🇹🇳"},
            {"name": "Zambie", "code": "ZMB", "phone_code": "260", "flag_emoji": "🇿🇲"},
            {"name": "Zimbabwe", "code": "ZWE", "phone_code": "263", "flag_emoji": "🇿🇼"},
        ]

        created_count = 0
        updated_count = 0

        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults=country_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Créé: {country.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Déjà existe: {country.name}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nTerminé! {created_count} pays créés, {updated_count} déjà existants.'
            )
        )
