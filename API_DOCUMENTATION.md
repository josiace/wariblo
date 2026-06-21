# API Documentation - Wariblo

## Base URL
```
http://localhost:4000/api/
```

## Authentication

### Register
**POST** `/api/auth/register/`

Créer un nouveau compte utilisateur.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "password_confirm": "password123",
  "role": "influencer",
  "phone_number": "+1234567890",
  "country": "SN"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "role": "influencer",
    "phone_number": "+1234567890",
    "country": "SN",
    "is_profile_complete": false,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "token": "abc123def456"
}
```

### Login
**POST** `/api/auth/login/`

Se connecter avec email et mot de passe.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "role": "influencer",
    "phone_number": "+1234567890",
    "country": "SN",
    "is_profile_complete": false,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "token": "abc123def456"
}
```

### Logout
**POST** `/api/auth/logout/`

Se déconnecter (supprime le token).

**Headers:**
```
Authorization: Token abc123def456
```

**Response:**
```json
{
  "message": "Déconnexion réussie"
}
```

## Endpoints

### Users
**GET** `/api/users/`
- Liste tous les utilisateurs (authentifié requis)
- Filtres: `role`, `country`
- Recherche: `email`, `username`, `full_name`

**GET** `/api/users/me/`
- Récupérer le profil de l'utilisateur connecté

### Influencers
**GET** `/api/influencers/`
- Liste tous les influenceurs (authentifié requis)
- Filtres: `niche`, `location`
- Recherche: `full_name`, `bio`
- Tri: `created_at`, `instagram_followers`

**POST** `/api/influencers/`
- Créer un profil influenceur

**GET** `/api/influencers/my_profile/`
- Récupérer le profil de l'influenceur connecté

### Advertisers
**GET** `/api/advertisers/`
- Liste tous les annonceurs (authentifié requis)
- Filtres: `industry`, `location`
- Recherche: `company_name`, `company_description`

**POST** `/api/advertisers/`
- Créer un profil annonceur

**GET** `/api/advertisers/my_profile/`
- Récupérer le profil de l'annonceur connecté

### Campaigns
**GET** `/api/campaigns/`
- Liste toutes les campagnes (authentifié requis)
- Filtres: `niche`, `platform`, `status`, `deadline`
- Recherche: `title`, `description`, `requirements`
- Tri: `created_at`, `budget`, `deadline`

**POST** `/api/campaigns/`
- Créer une nouvelle campagne (annonceur uniquement)

**GET** `/api/campaigns/{id}/`
- Récupérer les détails d'une campagne

**GET** `/api/campaigns/{id}/applications/`
- Récupérer les applications pour une campagne

**GET** `/api/campaigns/my_campaigns/`
- Récupérer les campagnes de l'annonceur connecté

### Applications
**GET** `/api/applications/`
- Liste toutes les candidatures (authentifié requis)
- Filtres: `status`, `campaign`, `influencer`
- Recherche: `pitch`
- Tri: `created_at`, `proposed_price`

**POST** `/api/applications/`
- Créer une nouvelle candidature (influenceur uniquement)

**GET** `/api/applications/{id}/`
- Récupérer les détails d'une candidature

**GET** `/api/applications/my_applications/`
- Récupérer les candidatures de l'influenceur connecté

### Conversations
**GET** `/api/conversations/`
- Liste toutes les conversations (authentifié requis)
- Filtres: `participants`

**POST** `/api/conversations/`
- Créer une nouvelle conversation

**GET** `/api/conversations/my_conversations/`
- Récupérer les conversations de l'utilisateur connecté

**GET** `/api/conversations/{id}/messages/`
- Récupérer les messages d'une conversation

### Messages
**GET** `/api/messages/`
- Liste tous les messages (authentifié requis)
- Filtres: `conversation`, `is_read`
- Tri: `created_at`

**POST** `/api/messages/`
- Créer un nouveau message

**GET** `/api/messages/{id}/`
- Récupérer les détails d'un message

### Reviews
**GET** `/api/reviews/`
- Liste tous les avis (authentifié requis)
- Filtres: `rating`, `campaign`
- Recherche: `comment`
- Tri: `created_at`, `rating`

**POST** `/api/reviews/`
- Créer un nouvel avis

**GET** `/api/reviews/my_reviews/`
- Récupérer les avis de l'utilisateur connecté

**GET** `/api/reviews/reviews_about_me/`
- Récupérer les avis sur l'utilisateur connecté

### Campaign Analytics
**GET** `/api/campaign-analytics/`
- Liste toutes les analytics de campagnes (authentifié requis)
- Filtres: `campaign`

**GET** `/api/campaign-analytics/{id}/`
- Récupérer les analytics d'une campagne

### User Activities
**GET** `/api/user-activities/`
- Liste toutes les activités utilisateurs (authentifié requis)
- Filtres: `user`, `activity_type`, `campaign`

**GET** `/api/user-activities/my_activities/`
- Récupérer les activités de l'utilisateur connecté

### Countries
**GET** `/api/countries/`
- Liste tous les pays (pas d'authentification requise)
- Filtres: `is_active`
- Recherche: `name`, `code`

**GET** `/api/countries/{id}/`
- Récupérer les détails d'un pays

### Currencies
**GET** `/api/currencies/`
- Liste toutes les devises (pas d'authentification requise)
- Filtres: `is_active`
- Recherche: `name`, `code`, `symbol`

**GET** `/api/currencies/{id}/`
- Récupérer les détails d'une devise

### Subscription Plans
**GET** `/api/subscription-plans/`
- Liste tous les plans d'abonnement (pas d'authentification requise)
- Filtres: `plan_type`, `user_type`, `is_active`

**GET** `/api/subscription-plans/{id}/`
- Récupérer les détails d'un plan d'abonnement

### Subscriptions
**GET** `/api/subscriptions/`
- Liste tous les abonnements (authentifié requis)
- Filtres: `user`, `plan`, `status`

**GET** `/api/subscriptions/my_subscription/`
- Récupérer l'abonnement de l'utilisateur connecté

**GET** `/api/subscriptions/{id}/`
- Récupérer les détails d'un abonnement

### Transactions
**GET** `/api/transactions/`
- Liste toutes les transactions (authentifié requis)
- Filtres: `user`, `subscription`, `transaction_type`, `status`
- Tri: `created_at`

**GET** `/api/transactions/my_transactions/`
- Récupérer les transactions de l'utilisateur connecté

**GET** `/api/transactions/{id}/`
- Récupérer les détails d'une transaction

### Payment Methods
**GET** `/api/payment-methods/`
- Liste toutes les méthodes de paiement (authentifié requis)
- Filtres: `method_type`, `is_active`

**GET** `/api/payment-methods/{id}/`
- Récupérer les détails d'une méthode de paiement

### Manual Payments
**GET** `/api/manual-payments/`
- Liste tous les paiements manuels (authentifié requis)
- Filtres: `user`, `subscription_plan`, `payment_method`, `status`
- Tri: `created_at`

**POST** `/api/manual-payments/`
- Créer un nouveau paiement manuel

**GET** `/api/manual-payments/my_payments/`
- Récupérer les paiements manuels de l'utilisateur connecté

**GET** `/api/manual-payments/{id}/`
- Récupérer les détails d'un paiement manuel

### Site Settings
**GET** `/api/site-settings/`
- Liste tous les paramètres du site (pas d'authentification requise)

**GET** `/api/site-settings/current/`
- Récupérer les paramètres actuels du site

## Authentication

Pour accéder aux endpoints protégés, incluez le token dans le header:

```
Authorization: Token votre_token_ici
```

## Pagination

La plupart des endpoints supportent la pagination avec les paramètres:
- `page`: numéro de page
- `page_size`: nombre d'éléments par page (défaut: 20)

## Filtrage

Utilisez les paramètres de query pour filtrer les résultats:
```
/api/campaigns/?niche=fashion&platform=instagram&status=open
```

## Recherche

Utilisez le paramètre `search` pour rechercher:
```
/api/influencers/?search=fashion
```

## Tri

Utilisez le paramètre `ordering` pour trier les résultats:
```
/api/campaigns/?ordering=-created_at
```

## Erreurs

### 400 Bad Request
```json
{
  "error": "Message d'erreur"
}
```

### 401 Unauthorized
```json
{
  "detail": "Informations d'authentification non fournies."
}
```

### 404 Not Found
```json
{
  "detail": "Non trouvé."
}
```

### 403 Forbidden
```json
{
  "detail": "Vous n'avez pas la permission d'effectuer cette action."
}
```

## Rate Limiting

L'API utilise Django Axes pour le rate limiting:
- 5 tentatives de connexion échouées
- Délai de 30 minutes avant réinitialisation
