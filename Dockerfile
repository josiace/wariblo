FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles /app/mediafiles

EXPOSE 8000

# Le superutilisateur doit etre cree manuellement via :
#   python manage.py createsuperuser
# ou via create_admin.py avec les variables DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_PASSWORD.
CMD ["sh", "-c", "python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py load_countries && \
    python manage.py load_currencies && \
    gunicorn wariblo.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]
