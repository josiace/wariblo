# Système de Paiement Manuel - Wariblo

## 📋 Vue d'ensemble

Ce document explique le fonctionnement du système de paiement manuel implémenté pour Wariblo, adapté au contexte du Mali où l'accès aux API de paiement est difficile.

## 🏗️ Architecture du Système

### Modèles de Données

#### 1. PaymentMethod
Représente les méthodes de paiement disponibles pour les utilisateurs.

**Champs:**
- `name`: Nom de la méthode de paiement (ex: "Orange Money Mali")
- `method_type`: Type de paiement (bank_transfer, mobile_money, cash, check)
- `description`: Description détaillée
- `account_number`: Numéro de compte (pour virements)
- `phone_number`: Numéro de téléphone (pour mobile money)
- `bank_name`: Nom de la banque
- `instructions`: Instructions de paiement
- `is_active`: Statut d'activation

#### 2. ManualPayment
Représente les paiements manuels soumis par les utilisateurs.

**Champs:**
- `user`: Utilisateur qui effectue le paiement
- `subscription_plan`: Plan d'abonnement choisi
- `payment_method`: Méthode de paiement utilisée
- `amount`: Montant du paiement
- `currency`: Devise
- `status`: Statut (pending, confirmed, rejected, cancelled)
- `proof_document`: Preuve de paiement (fichier)
- `transaction_reference`: Référence de transaction
- `payment_date`: Date du paiement
- `notes`: Notes supplémentaires
- `reviewed_by`: Administrateur qui a validé
- `reviewed_at`: Date de validation
- `rejection_reason`: Raison du rejet

## 🔄 Flux de Travail

### 1. Utilisateur - Demande d'abonnement

1. **Sélection du plan**
   - L'utilisateur accède à la page des plans d'abonnement
   - Il sélectionne un plan (Gratuit, Pro, Enterprise)
   - Il clique sur "S'abonner"

2. **Formulaire de paiement**
   - L'utilisateur remplit le formulaire de paiement manuel
   - Il sélectionne une méthode de paiement (Orange Money, Wave, etc.)
   - Il peut fournir:
     - Référence de transaction
     - Date de paiement
     - Preuve de paiement (capture d'écran)
     - Notes

3. **Soumission**
   - Le système crée un `ManualPayment` avec le statut `pending`
   - L'utilisateur est redirigé vers "Mon abonnement"
   - Un message de confirmation s'affiche

### 2. Administrateur - Validation des paiements

1. **Accès à l'interface admin**
   - L'administrateur se connecte au panel Django Admin
   - Il accède à la section "Paiements manuels"

2. **Vérification des paiements**
   - L'administrateur voit la liste des paiements en attente
   - Il peut vérifier:
     - Les preuves de paiement
     - Les références de transaction
     - Les notes de l'utilisateur

3. **Validation**
   - **Approbation**: L'administrateur sélectionne les paiements et clique sur "Approuver"
     - Le système crée automatiquement l'abonnement
     - Le système crée la transaction
     - Le statut du passe à `confirmed`
   - **Rejet**: L'administrateur peut rejeter avec une raison
     - Le statut passe à `rejected`
     - L'utilisateur peut soumettre une nouvelle demande

### 3. Activation de l'abonnement

Lorsqu'un paiement est approuvé:
1. Création d'un `Subscription` avec le statut `active`
2. Date de début: date d'approbation
3. Date de fin: date de début + 30 jours
4. Création d'une `Transaction` de type `subscription`
5. L'utilisateur accède immédiatement aux fonctionnalités du plan

## 💳 Méthodes de Paiement Disponibles

### Méthodes Préconfigurées pour le Mali

1. **Orange Money Mali**
   - Type: Mobile Money
   - Instructions: Envoyer le montant via Orange Money

2. **Wave Mali**
   - Type: Mobile Money
   - Instructions: Envoyer le montant via Wave

3. **Malitel Money**
   - Type: Mobile Money
   - Instructions: Envoyer le montant via Malitel Money

4. **Virement bancaire BDM SA**
   - Type: Virement bancaire
   - Instructions: Effectuer un virement vers le compte BDM SA

5. **Virement bancaire Ecobank Mali**
   - Type: Virement bancaire
   - Instructions: Effectuer un virement vers le compte Ecobank Mali

6. **Espèces**
   - Type: Espèces
   - Instructions: Contacter pour paiement au bureau

## 🛠️ Configuration

### Charger les méthodes de paiement par défaut

```bash
python manage.py load_payment_methods
```

Cette commande charge les méthodes de paiement préconfigurées pour le Mali.

### Ajouter une nouvelle méthode de paiement

Via l'interface Django Admin:
1. Accéder à "Méthodes de paiement"
2. Cliquer sur "Ajouter"
3. Remplir les informations
4. Sauvegarder

## 📊 Limitations par Plan

### Plan Gratuit
- **Messages**: 50 par jour
- **Conversations**: 10 simultanées
- **Contenu**: Pas de numéros de téléphone, pas de liens externes, pas de mots-clés de contact

### Plan Payant (Pro/Enterprise)
- **Messages**: Illimité
- **Conversations**: Illimité
- **Contenu**: Censure automatique des coordonnées

## 🔒 Sécurité

### Validation des messages
- **Plan gratuit**: Blocage des messages contenant:
  - Séquences de chiffres > 4
  - Patterns de téléphone
  - Mots-clés de contact (WhatsApp, email, etc.)
  - Liens externes

- **Plan payant**: Censure automatique des coordonnées

### Limites de messages
- Vérification du nombre de messages envoyés par jour
- Message d'erreur si limite atteinte

### Limites de conversations
- Vérification du nombre de conversations simultanées
- Message d'erreur si limite atteinte

## 📝 Commandes Management

### Charger les méthodes de paiement
```bash
python manage.py load_payment_methods
```

### Charger les plans d'abonnement
```bash
python manage.py load_subscription_plans
```

## 🎯 Points d'Intégration

### URLs disponibles
- `/billing/pricing/` - Liste des plans d'abonnement
- `/billing/subscribe/<plan_id>/` - Formulaire de paiement
- `/billing/subscription/my/` - Mon abonnement
- `/billing/subscription/cancel/<subscription_id>/` - Annuler l'abonnement
- `/billing/transactions/` - Historique des transactions

### Templates
- `billing/pricing_plans.html` - Liste des plans
- `billing/request_subscription.html` - Formulaire de paiement
- `billing/my_subscription.html` - Mon abonnement
- `billing/cancel_subscription.html` - Annulation
- `billing/transactions_history.html` - Historique

## 🔧 Maintenance

### Surveillance des paiements
- Vérifier régulièrement les paiements en attente
- Valider rapidement les paiements valides
- Communiquer avec les utilisateurs en cas de problème

### Rapports
- Générer des rapports de paiements mensuels
- Suivre les statistiques d'abonnement
- Identifier les méthodes de paiement les plus utilisées

## 📞 Support

Pour toute question sur le système de paiement:
1. Consulter ce document
2. Vérifier les logs Django
3. Contacter l'équipe technique

## 🚀 Améliorations Futures

- Système de facturation PDF
- Notifications automatiques par email
- Intégration avec des API de paiement (si disponible)
- Système de rappel pour les paiements en attente
- Tableau de bord de statistiques de paiement
