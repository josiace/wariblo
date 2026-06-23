import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wariblo.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Créer un superuser avec des identifiants par défaut
email = 'afletounoudouprince5@gmail.com'
password = 'waribloprince5@gmail'

if not User.objects.filter(email=email).exists():
    user = User.objects.create_user(
        email=email,
        password=password,
        role='admin',
        is_staff=True,
        is_superuser=True
    )
    print(f"Superuser créé avec succès!")
    print(f"Email: {email}")
    print(f"Mot de passe: {password}")
else:
    print(f"Un utilisateur avec l'email {email} existe déjà.")
