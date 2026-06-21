#!/bin/bash

# Script de déploiement pour Wariblo
# Ce script automatise le processus de déploiement en production

set -e

echo "🚀 Début du déploiement de Wariblo..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé. Création à partir de .env.example..."
    cp .env.example .env
    echo "⚠️  Veuillez éditer le fichier .env avec vos configurations de production avant de continuer."
    echo "⚠️  IMPORTANT: Changez SECRET_KEY, DB_PASSWORD, et autres configurations sensibles."
    read -p "Appuyez sur Entrée une fois que vous avez configuré .env..."
fi

# Créer les répertoires nécessaires
echo "📁 Création des répertoires nécessaires..."
mkdir -p ssl staticfiles mediafiles logs

# Générer une clé secrète si nécessaire
if grep -q "your-secret-key-here" .env; then
    echo "🔑 Génération d'une nouvelle clé secrète..."
    SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    sed -i "s/your-secret-key-here-generate-with-python-manage-py-generatesecretkey/$SECRET_KEY/" .env
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Construire les images Docker
echo "🔨 Construction des images Docker..."
docker-compose build

# Exécuter les migrations
echo "📊 Exécution des migrations..."
docker-compose run --rm web python manage.py migrate

# Collecter les fichiers statiques
echo "📦 Collecte des fichiers statiques..."
docker-compose run --rm web python manage.py collectstatic --noinput

# Créer un superutilisateur si nécessaire
echo "👤 Création d'un superutilisateur..."
docker-compose run --rm web python manage.py createsuperuser --noinput --username admin --email admin@wariblo.com || true

# Charger les données initiales
echo "📥 Chargement des données initiales..."
docker-compose run --rm web python manage.py load_currencies
docker-compose run --rm web python manage.py load_payment_methods
docker-compose run --rm web python manage.py load_subscription_plans

# Démarrer les conteneurs
echo "🚀 Démarrage des conteneurs..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente des services..."
sleep 10

# Vérifier l'état des conteneurs
echo "🔍 Vérification de l'état des conteneurs..."
docker-compose ps

# Afficher les logs
echo "📋 Logs des services..."
docker-compose logs --tail=20

echo "✅ Déploiement terminé avec succès !"
echo "🌐 L'application est accessible sur http://localhost"
echo "📊 Admin accessible sur http://localhost/admin"
echo "📚 API disponible sur http://localhost/api"
echo ""
echo "Pour voir les logs en temps réel: docker-compose logs -f"
echo "Pour arrêter les services: docker-compose down"
echo "Pour redémarrer les services: docker-compose restart"
