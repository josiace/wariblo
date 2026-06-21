# Dockerfile pour le déploiement de Wariblo
FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Créer le répertoire pour les fichiers statiques
RUN mkdir -p /app/staticfiles /app/mediafiles

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Commande de démarrage avec Gunicorn
CMD ["gunicorn", "wariblo.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
