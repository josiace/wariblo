# Guide de Déploiement - Wariblo

## Prérequis

- Docker et Docker Compose installés
- Git
- Domaine configuré (optionnel pour HTTPS)
- Certificat SSL (optionnel pour HTTPS)

## Configuration

### 1. Cloner le repository

```bash
git clone https://github.com/josiace/wariblo.git
cd wariblo
```

### 2. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Éditer le fichier `.env` avec vos configurations:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=wariblo
DB_USER=wariblo_user
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@wariblo.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Cache
CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
CACHE_LOCATION=redis://redis:6379/1

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 3. Générer une clé secrète

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copiez le résultat et collez-le dans `SECRET_KEY` dans `.env`.

### 4. Configuration SSL (optionnel mais recommandé)

Créer le répertoire `ssl/` et ajouter vos certificats:

```bash
mkdir ssl
# Copier vos certificats dans ssl/cert.pem et ssl/key.pem
```

Pour un certificat gratuit avec Let's Encrypt:

```bash
sudo apt-get install certbot
sudo certbot certonly --standalone -d your-domain.com
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
```

## Déploiement

### Méthode 1: Script Automatisé

```bash
chmod +x deploy.sh
./deploy.sh
```

### Méthode 2: Manuel

#### 1. Construire les images Docker

```bash
docker-compose build
```

#### 2. Exécuter les migrations

```bash
docker-compose run --rm web python manage.py migrate
```

#### 3. Collecter les fichiers statiques

```bash
docker-compose run --rm web python manage.py collectstatic --noinput
```

#### 4. Créer un superutilisateur

```bash
docker-compose run --rm web python manage.py createsuperuser
```

#### 5. Charger les données initiales

```bash
docker-compose run --rm web python manage.py load_currencies
docker-compose run --rm web python manage.py load_payment_methods
docker-compose run --rm web python manage.py load_subscription_plans
```

#### 6. Démarrer les services

```bash
docker-compose up -d
```

## Vérification

### Vérifier l'état des conteneurs

```bash
docker-compose ps
```

### Voir les logs

```bash
docker-compose logs -f
```

### Vérifier les logs spécifiques

```bash
docker-compose logs web
docker-compose logs nginx
docker-compose logs db
```

### Tests de santé

```bash
curl http://localhost/health/
```

## Gestion

### Arrêter les services

```bash
docker-compose down
```

### Redémarrer les services

```bash
docker-compose restart
```

### Mettre à jour l'application

```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py collectstatic --noinput
```

### Sauvegarder la base de données

```bash
docker-compose exec db pg_dump -U wariblo_user wariblo > backup.sql
```

### Restaurer la base de données

```bash
docker-compose exec -T db psql -U wariblo_user wariblo < backup.sql
```

## Surveillance

### Voir l'utilisation des ressources

```bash
docker stats
```

### Voir les logs en temps réel

```bash
docker-compose logs -f web
```

### Accéder au conteneur

```bash
docker-compose exec web bash
```

## Sécurité

### Mises à jour de sécurité

```bash
docker-compose pull
docker-compose up -d
```

### Configuration du pare-feu

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Rotation des logs

Configurer logrotate pour les logs Docker:

```bash
sudo nano /etc/logrotate.d/docker
```

Contenu:
```
/var/lib/docker/containers/*/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
}
```

## Dépannage

### Erreur de connexion à la base de données

```bash
docker-compose restart db
docker-compose logs db
```

### Erreur de permissions sur les fichiers statiques

```bash
sudo chown -R $USER:$USER staticfiles mediafiles
```

### Problèmes de mémoire

```bash
docker-compose down
docker system prune -a
docker-compose up -d
```

### Vérifier les erreurs dans les logs

```bash
docker-compose logs web | grep ERROR
```

## Performance

### Optimisation de la base de données

```bash
docker-compose exec db psql -U wariblo_user wariblo -c "VACUUM ANALYZE;"
```

### Nettoyer les anciennes images Docker

```bash
docker image prune -a
```

### Nettoyer les volumes inutilisés

```bash
docker volume prune
```

## Monitoring

### Installation de monitoring (optionnel)

Prometheus + Grafana pour le monitoring:

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

## Backup Automatisé

Créer un cron job pour les sauvegardes automatiques:

```bash
sudo crontab -e
```

Ajouter:
```
0 2 * * * cd /path/to/wariblo && docker-compose exec db pg_dump -U wariblo_user wariblo > backup_$(date +\%Y\%m\%d).sql
```

## Support

Pour les problèmes de déploiement:
- Vérifier les logs: `docker-compose logs`
- Vérifier l'état: `docker-compose ps`
- Consulter la documentation: [Documentation Django](https://docs.djangoproject.com/)
