import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wariblo.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Creation d'un superutilisateur uniquement a partir des variables d'environnement.
# Aucun identifiant n'est stocke dans le depot.
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not email or not password:
    print('DJANGO_SUPERUSER_EMAIL ou DJANGO_SUPERUSER_PASSWORD non definis : aucun superutilisateur cree.')
elif not User.objects.filter(email=email).exists():
    User.objects.create_user(
        email=email,
        password=password,
        role='admin',
        is_staff=True,
        is_superuser=True
    )
    print('Superutilisateur cree avec succes.')
else:
    print('Un utilisateur avec cet email existe deja.')
