# Guide de Déploiement Gratuit - Wariblo

## 🆓 Meilleures Plateformes Gratuites pour Django

### 1. PythonAnywhere (Recommandé pour débutants)
- **Gratuit**: Oui
- **Limites**: 1 application web, base de données SQLite
- **Avantages**: Très simple, support Django natif
- **Inconvénients**: Pas de PostgreSQL gratuit, limité

### 2. Render (Recommandé)
- **Gratuit**: Oui
- **Limites**: 512MB RAM, sleep après inactivité
- **Avantages**: PostgreSQL gratuit, Docker support
- **Inconvénients**: Application dort après 15min d'inactivité

### 3. Railway
- **Gratuit**: Oui ($5 crédit mensuel)
- **Limites**: 512MB RAM, 500h d'utilisation
- **Avantages**: PostgreSQL gratuit, très moderne
- **Inconvénients**: Crédits limités

### 4. Fly.io
- **Gratuit**: Oui
- **Limites**: 3 VMs, 256MB RAM chacune
- **Avantages**: Docker natif, mondial
- **Inconvénients**: Configuration complexe

## 🚀 Déploiement sur PythonAnywhere (Le plus simple)

### Étape 1: Créer un compte
1. Allez sur [pythonanywhere.com](https://www.pythonanywhere.com)
2. Créez un compte gratuit (Beginner account)
3. Vérifiez votre email

### Étape 2: Créer une application web
1. Allez dans "Web" → "Add a new web app"
2. Choisissez "Manual configuration"
3. Choisissez Python 3.11
4. Configurez le chemin: `/home/votre_username/wariblo`

### Étape 3: Uploader le code
```bash
# Sur votre machine locale
git clone https://github.com/josiace/wariblo.git
cd wariblo
zip -r wariblo.zip .
```

Puis sur PythonAnywhere:
1. Allez dans "Files"
2. Uploadez `wariblo.zip`
3. Décompressez-le

### Étape 4: Configurer l'environnement virtuel
Sur PythonAnywhere:
```bash
mkvirtualenv --python=/usr/bin/python3.11 wariblo
pip install -r requirements.txt
```

### Étape 5: Configurer la base de données
PythonAnywhere utilise SQLite par défaut (gratuit):
```bash
# Pas de configuration nécessaire
# SQLite sera utilisé automatiquement
```

### Étape 6: Configurer les variables d'environnement
Dans "Web" → "Variables":
```
DEBUG=False
SECRET_KEY=votre_clé_secrète
ALLOWED_HOSTS=votre_username.pythonanywhere.com
```

### Étape 7: Configurer WSGI
Dans "Web" → "WSGI configuration file":
```python
import os
import sys

path = '/home/votre_username/wariblo'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'wariblo.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Étape 8: Migrations et fichiers statiques
```bash
cd /home/votre_username/wariblo
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Étape 9: Configurer les fichiers statiques
Dans "Web" → "Static files":
- URL: `/static/`
- Directory: `/home/votre_username/wariblo/staticfiles`

### Étape 10: Redémarrer
Cliquez sur "Reload" dans la section Web

## 🚀 Déploiement sur Render (Moderne avec PostgreSQL)

### Étape 1: Créer un compte
1. Allez sur [render.com](https://render.com)
2. Créez un compte gratuit avec GitHub
3. Connectez votre repository GitHub

### Étape 2: Adapter le projet pour Render

Créez un fichier `render.yaml`:
```yaml
services:
  - type: web
    name: wariblo
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn wariblo.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: wariblo-db
          property: connectionString
      - key: SECRET_KEY
        generate: true
      - key: DEBUG
        value: "False"
      - key: ALLOWED_HOSTS
        value: "*.onrender.com"

databases:
  - name: wariblo-db
    databaseName: wariblo
    user: wariblo
```

### Étape 3: Modifier settings.py pour Render
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True
    )
}
```

### Étape 4: Ajouter les dépendances
Dans `requirements.txt`:
```
dj-database-url==2.1.0
gunicorn==21.2.0
whitenoise==6.6.0
```

### Étape 5: Push sur GitHub
```bash
git add .
git commit -m "Configuration pour Render"
git push origin main
```

### Étape 6: Déployer sur Render
1. Allez sur Render → "New" → "Web Service"
2. Connectez votre repository GitHub
3. Render détectera automatiquement le fichier `render.yaml`
4. Cliquez sur "Create Web Service"

### Étape 7: Créer un superutilisateur
```bash
# Dans Render Shell
python manage.py createsuperuser
```

## 🚀 Déploiement sur Railway (Moderne)

### Étape 1: Créer un compte
1. Allez sur [railway.app](https://railway.app)
2. Créez un compte gratuit avec GitHub
3. Connectez votre repository

### Étape 2: Créer un projet
1. Cliquez sur "New Project"
2. Choisissez "Deploy from GitHub repo"
3. Sélectionnez votre repository

### Étape 3: Ajouter des services
- **PostgreSQL**: Cliquez sur "+" → "Database" → "PostgreSQL"
- **Web Service**: Cliquez sur "+" → "New Service" → "Dockerfile"

### Étape 4: Configurer les variables
Dans les variables d'environnement:
```
DATABASE_URL=postgresql://...
SECRET_KEY=votre_clé_secrète
DEBUG=False
ALLOWED_HOSTS=votre-app.railway.app
```

### Étape 5: Déployer
Railway déploiera automatiquement

## 🚀 Déploiement sur Fly.io (Docker)

### Étape 1: Installer Fly CLI
```bash
# Sur votre machine locale
curl -L https://fly.io/install.sh | sh
```

### Étape 2: Se connecter
```bash
fly auth login
```

### Étape 3: Lancer l'application
```bash
fly launch
```

### Étape 4: Configurer
Répondez aux questions:
- App name: wariblo
- Region: choisissez la plus proche (cdg pour Paris)
- Database: PostgreSQL

### Étape 5: Déployer
```bash
fly deploy
```

## 📊 Comparaison des Plateformes Gratuites

| Plateforme | RAM | Base de données | Sleep | Difficulté |
|-----------|-----|----------------|-------|------------|
| PythonAnywhere | Illimitée | SQLite | Non | ⭐ Très facile |
| Render | 512MB | PostgreSQL | Oui (15min) | ⭐⭐ Facile |
| Railway | 512MB | PostgreSQL | Non | ⭐⭐ Facile |
| Fly.io | 256MB | PostgreSQL | Non | ⭐⭐⭐ Moyen |

## 💡 Recommandation

**Pour débutant**: PythonAnywhere
- Le plus simple
- Pas de configuration complexe
- Support Django natif

**Pour moderne**: Render
- PostgreSQL gratuit
- Interface moderne
- Intégration GitHub

**Pour professionnel**: Railway
- Plus de fonctionnalités
- Meilleure performance
- Support Docker

## 🔧 Configuration Adaptée pour Plateformes Gratuites

### Modifications nécessaires dans settings.py:

```python
# Pour toutes les plateformes gratuites
import os
import dj_database_url

# Base de données flexible
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True
    )
}

# Fichiers statiques avec WhiteNoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... autres middlewares
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Sécurité adaptée
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Désactivé pour plateformes gratuites
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
```

### Ajouter dans requirements.txt:
```
dj-database-url==2.1.0
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
```

## 🎯 Mon Choix: Render

**Pourquoi Render:**
- PostgreSQL gratuit
- Interface moderne
- Intégration GitHub automatique
- SSL gratuit
- Domaine gratuit: `votre-app.onrender.com`

**Étapes rapides:**
1. Créer un compte Render
2. Connecter GitHub
3. Ajouter le fichier `render.yaml`
4. Push les modifications
5. Render déploie automatiquement

C'est la meilleure option gratuite moderne pour Django !
