from django.contrib import admin
from django.utils.html import format_html

from core.models import Subscription, SubscriptionPlan, Transaction

# Les modèles SubscriptionPlan, Subscription et Transaction sont déjà enregistrés dans core/admin.py
# Ce fichier est conservé pour compatibilité mais ne contient plus d'enregistrements en double
